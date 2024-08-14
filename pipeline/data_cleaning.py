from pyspark.sql import SparkSession

def clean_text_data(input_file, output_file):
    spark = SparkSession.builder.appName("DataCleaning").getOrCreate()
    df = spark.read.json(input_file)
    # Perform text cleaning steps here (e.g., removing stopwords, tokenization)
    # For now, let's just select the title and content
    df_clean = df.select('title', 'content')
    df_clean.write.json(output_file)
    spark.stop()

if __name__ == "__main__":
    clean_text_data('scraping/output.json', 'pipeline/cleaned_data.json')
