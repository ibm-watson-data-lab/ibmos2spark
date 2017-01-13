
lazy val commonSettings = Seq(
  organization := "com.ibm",
  scalaVersion := "2.11.7"
)

lazy val root = (project in file("."))
  .aggregate(spark16, spark20)

lazy val spark16 = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    name := "ibmos2spark",
    version := "0.1.6",
    libraryDependencies ++= {
      val sparkVersion =  "1.6.0"
      Seq(
        "org.apache.spark" %%  "spark-core"   %  sparkVersion % "provided"
      )
    }
  )

lazy val spark20 = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    name := "ibmos2spark",
    version := "0.2.0",
    libraryDependencies ++= {
      val sparkVersion =  "2.0.0"
      Seq(
        "org.apache.spark" %%  "spark-core"   %  sparkVersion % "provided"
      )
    }
  )

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)