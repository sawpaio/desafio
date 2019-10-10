import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.SparkSession
import spark.implicits._

object processamento_spark
{
    def main(args: Array[String])
    {

     // Configuração padrão
    val spark = SparkSession.builder.appName("processamento_spark").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

     // Dataframes dos resultados dos crawlers
    val dolar = spark.read.format("csv").option("header", "true").option("delimiter", ",").load("/user/lucasSampaio/dolar_data.csv");
    val crypto = spark.read.format("csv").option("header", "true").option("delimiter",",").load("/user/lucasSampaio/crypto_timestamp.csv");
    
    //Drop no timestamp da tabela Crypto.
    val crypto_formatado = crypto.drop("timestamp")
    //Drop dos campos que não serão usados na tabela Dolar.
    val dolar_formatado = dolar.drop("currency", "change", "perc")
        
    //Cross Join de crypto_sem_timestamp com dolar_formatado.
    val dolar_com_crypto = dolar_formatado.crossJoin(crypto_formatado)
    
    //Função que multiplica o dólar pelo real Brasileiro.
    val dolar_mult_real : (Float, Float) => Float = (priceUSD:Float, value:Float) => {priceUSD * value};
    
    //Método para criar uma variável pelo resultado formado pela função dolar_para_real.
    val dolar_mult_realUDF = udf(dolar_mult_real);

    //Criando novo dataset com o valor do Dólar em multiplicado pelo Real. 
    val processo_final = dolar_com_crypto.withColumn("priceReal",dolar_mult_realUDF(dolar_com_crypto.col("priceUSD"),dolar_com_crypto.col("value")));

    //Ordenando as colunas
    val dataset_finalizado = processo_final.select("code", "symbol", "name", "priceUSD", "priceReal", "priceBTC", "change24H", "volume24H", "timestamp");
    
    
    //Salvando o dataset em Json na pasta indicada pelo esquema de diretorios.
    dataset_finalizado.write.json("/user/lucasSampaio/output/processado_data.json");
    dataset_finalizado.json("/user/lucasSampaio/output/transferidos/processado_data.json");
    System.exit(0)

    }
}

