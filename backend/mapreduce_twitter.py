from pyspark import SparkContext, SparkConf
import os

# Global SparkContext instance (singleton pattern) - necessary!!
_spark_context = None

def get_spark_context():
    """Get or create a singleton SparkContext instance."""
    global _spark_context
    if _spark_context is None:
        # Configure Spark for S3 access
        conf = SparkConf().setAppName("TwitterFollowerCount")
        
        # Configure S3A filesystem with anonymous access (bucket is public)
        conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        conf.set("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider")
        
        _spark_context = SparkContext(conf=conf)
    return _spark_context

def mapreduce_twitter(file_path: str):
    sc = get_spark_context()
    
    # Support both local files and S3 paths
    # If file_path doesn't start with s3://, treat it as local
    if not file_path.startswith("s3://"):
        # Check if AWS credentials are available for S3
        s3_bucket = os.environ.get("S3_BUCKET", "sneha-lab1-photo-public")
        file_path = f"s3a://{s3_bucket}/twitter_combined.txt"

    # Each line: userA userB → userA follows userB
    data = sc.textFile(file_path)
    edges = data.map(lambda line: line.strip().split())

    # Count followers: how many follow each user (userB)
    followers = edges.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)

    # Count followees: how many users each user follows (userA)
    followees = edges.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)

    # Combine results
    combined = followers.fullOuterJoin(followees).mapValues(
        lambda x: {
            "followers": x[0] if x[0] is not None else 0,
            "followees": x[1] if x[1] is not None else 0
        }
    )

    results = combined.collect()
    # Don't stop the context - reuse it for future requests
    # sc.stop()

    return dict(results)
