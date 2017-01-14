name := "ibmos2spark"

organization := "com.ibm"

version := "0.1"

scalaVersion := "2.11.8"

crossScalaVersions := Seq("2.10.4", "2.11.8") 

libraryDependencies ++= {
  val sparkVersion =  if (scalaVersion.value == "2.11.8") "2.0.2" else "1.6.0"
  Seq(
    "org.apache.spark" %%  "spark-core"   %  sparkVersion % "provided"
  )
}

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)

