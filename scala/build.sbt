name := "ibmos2spark"

organization := "com.ibm"

version := "0.1"

scalaVersion := "2.11.7"

libraryDependencies ++= {
  val sparkVersion =  "1.6.0"
  Seq(
    "org.apache.spark" %%  "spark-core"   %  sparkVersion % "provided",
    "org.apache.spark" %%  "spark-sql"    %  sparkVersion % "provided",
    "org.apache.spark" %% "spark-repl" % sparkVersion % "provided"
  )
}

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)