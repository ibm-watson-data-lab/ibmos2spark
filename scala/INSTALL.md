# Build and Publish instructions.

This serves as a simple document to remind developers of necessary SBT commands.

## Build Locally

The following will generate all of the source/javadoc and compiled code `.jars`. 

```
sbt +publishLocal
```

The following will `assemble` an uber `.jar`, which contains all depedency code

```
sbt +assembly
```

The `+` instructs SBT to perform the build for all Scala versions found in `crossScalaVersions` in 
the [build.sbt](build.sbt) file. 

The resulting `jar` files will be found in the `target` directory. 

## Publish

Publishing requires an account to the Central Repository and privileges to post to the /com/ibm/ibmos2spark
directory. 

See the instructions here: http://central.sonatype.org/pages/ossrh-guide.html

We use the `sbt-sonatype` plugin: https://github.com/xerial/sbt-sonatype

Once fully configured (you'll need a GPG key that is published along with your Sonatype account credentials
stored in `~/.sbt/<version>/sonatype.sbt`) you should be able to 

```
sbt +publishSigned
```

Note that if `version` (found in build.sbt) has the suffix `SNAPSHOT`, the jars will be uploaded to the Sonatype
SNAPSHOT repository instead of the main release repository. After pushing to the release repository, you still
need to perform the remaining steps to publish the code to the public

```
sbt +sonatypeRelease
```
