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