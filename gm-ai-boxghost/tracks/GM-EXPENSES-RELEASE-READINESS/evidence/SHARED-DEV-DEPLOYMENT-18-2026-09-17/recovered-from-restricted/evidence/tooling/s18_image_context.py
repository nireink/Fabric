"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - prepare the image build context from the committed Dockerfile's runtime stage.
The runtime stage of Gystigo@bcb9591 platform_os/server/Dockerfile is copied verbatim; only its COPY --from=build line is
replaced by a COPY of the proven artifact (same destination, same owner). Nothing in any repository is modified."""
import hashlib, io, os, shutil

S18 = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(S18, "build")
committed = io.open(os.path.join(B, "src", "Gystigo", "platform_os", "server", "Dockerfile"), encoding="utf-8").read().replace("\r\n", "\n")
start = committed.index("FROM eclipse-temurin:25-jre-noble AS runtime")
runtime = committed[start:]
original_copy = "COPY --from=build --chown=app:app /workspace/platform_os/server/target/gystigo-host-runtime-0.1.0-SNAPSHOT.jar /app/app.jar"
assert runtime.count(original_copy) == 1, "unexpected runtime stage"
deploy = runtime.replace(original_copy, "COPY --chown=app:app gystigo-host-runtime-0.1.0-SNAPSHOT.jar /app/app.jar")
header = ("# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - disposable deployment Dockerfile (never committed).\n"
          "# Runtime stage copied verbatim from Gystigo@bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f platform_os/server/Dockerfile;\n"
          "# the build stage is replaced by the artifact built from the clean commit exports (SHA-256 recorded in evidence).\n")
context = os.path.join(B, "image")
os.makedirs(context, exist_ok=True)
io.open(os.path.join(context, "Dockerfile"), "w", encoding="utf-8", newline="\n").write(header + deploy)
artifact = os.path.join(B, "src", "Gystigo", "platform_os", "server", "target", "gystigo-host-runtime-0.1.0-SNAPSHOT.jar")
shutil.copyfile(artifact, os.path.join(context, "gystigo-host-runtime-0.1.0-SNAPSHOT.jar"))
digest = hashlib.sha256(open(os.path.join(context, "gystigo-host-runtime-0.1.0-SNAPSHOT.jar"), "rb").read()).hexdigest()
diff_lines = [l for l in deploy.splitlines() if l not in runtime.splitlines()]
print("CONTEXT=%s\nARTIFACT_IN_CONTEXT_SHA256=%s\nRUNTIME_STAGE_LINES=%d CHANGED_LINES=%s" % (context, digest, len(runtime.splitlines()), diff_lines))
print("----- deployment Dockerfile")
print(io.open(os.path.join(context, "Dockerfile"), encoding="utf-8").read())
