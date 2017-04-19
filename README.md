# ibmos2spark

The package sets Spark Hadoop configurations for connecting to 
IBM Bluemix Object Storage and Softlayer Account Object Storage instances. This packages uses the new [stocator](https://github.com/SparkTC/stocator) driver, which implements the `swift2d` protocol, and is availble
on the latest IBM Apache Spark Service instances (and through IBM Data Science Experience). 


Using the `stocator` driver connects your Spark executor nodes directly 
to your data in object storage.
This is an optimized, high-performance method to connect Spark to your data. All IBM Apache Spark kernels
are instantiated with the `stocator` driver in the Spark kernel's classpath. 
You can also run this locally by installing the [stocator driver](https://github.com/SparkTC/stocator) 
and adding it to your local Apache Spark kernel's classpath. 


This repository contains separate packages for `python`, `R` and `scala`. 
You will find their documentation within the sub-folders.
