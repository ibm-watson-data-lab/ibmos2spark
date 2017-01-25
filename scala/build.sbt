name := "ibmos2spark"

organization := "com.ibm.ibmos2spark"

version := "0.0.7"

scalaVersion := "2.11.8"

crossScalaVersions := Seq("2.10.4", "2.11.8") 

libraryDependencies ++= {
  val sparkVersion =  if (scalaVersion.value == "2.11.8") "2.0.2" else "1.6.0"
  Seq(
    "org.apache.spark" %%  "spark-core"   %  sparkVersion % "provided"
  )
}

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)

// Your profile name of the sonatype account. The default is the same with the organization value
sonatypeProfileName := "com.ibm.ibmos2spark"

// To sync with Maven central, you need to supply the following information:
pomExtra in Global := {
  <url>https://github.com/ibm-cds-labs/ibmos2spark/</url>
  <licenses>
    <license>
      <name>Apache 2</name>
      <url>http://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <scm>
    <connection>scm:git:github.com/ibm-cds-labs/ibmos2spark</connection>
    <developerConnection>scm:git:git@github.com:ibm-cds-labs/ibmos2spark</developerConnection>
    <url>github.com/ibm-cds-labs/ibmos2spark</url>
  </scm>
  <developers>
    <developer>
      <id>gadamc</id>
      <name>G Adam Cox</name>
      <url>https://github.com/gadamc</url>
    </developer>
  </developers>
}


lazy val root = (project in file(".")).
  enablePlugins(BuildInfoPlugin).
  settings(
    buildInfoKeys := Seq[BuildInfoKey](name, version, scalaVersion, sbtVersion),
    buildInfoPackage := organization.value,
    buildInfoOptions += BuildInfoOption.ToMap,
    buildInfoOptions += BuildInfoOption.ToJson
  )
