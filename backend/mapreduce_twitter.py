from pyspark import SparkContext

# Global SparkContext instance (singleton pattern)
_spark_context = None

def get_spark_context():
    """Get or create a singleton SparkContext instance."""
    global _spark_context
    if _spark_context is None:
        _spark_context = SparkContext("local", "TwitterFollowerCount")
    return _spark_context

def mapreduce_twitter(file_path: str):
    sc = get_spark_context()

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
