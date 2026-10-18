# Kali is rolling. Set KALI_IMAGE to an approved repo@sha256 digest for a release.
# ttyd's exact upstream source commit is pinned; distro packages are inventoried.
ARG KALI_IMAGE=kalilinux/kali-rolling:latest
FROM ${KALI_IMAGE} AS ttyd-build
ARG TTYD_COMMIT=40e79c706be14029b391f369bee6613c31667abb
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git cmake build-essential pkg-config \
    libjson-c-dev libwebsockets-dev libwebsockets-evlib-uv libuv1-dev \
    && rm -rf /var/lib/apt/lists/*
RUN git init /src/ttyd && cd /src/ttyd \
    && git remote add origin https://github.com/tsl0922/ttyd.git \
    && git fetch --depth 1 origin "${TTYD_COMMIT}" \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "${TTYD_COMMIT}" \
    && cmake -S . -B build -DCMAKE_BUILD_TYPE=MinSizeRel -DCMAKE_INSTALL_PREFIX=/usr/local \
    && cmake --build build --parallel 2 \
    && cmake --install build
# Let dpkg discover ABI package names instead of guessing libwebsockets versions.
RUN cd /src/ttyd && mkdir -p debian \
    && printf 'Source: smartkea-ttyd\nSection: misc\nPriority: optional\nMaintainer: SmartKEA\n\nPackage: smartkea-ttyd\nArchitecture: any\nDescription: Terminal training binary\n' > debian/control \
    && dpkg-shlibdeps -O -e/usr/local/bin/ttyd \
       | sed -n 's/^shlibs:Depends=//p' \
       | sed 's/ ([^)]*)//g;s/,//g' > /tmp/ttyd-runtime-packages.txt \
    && test -s /tmp/ttyd-runtime-packages.txt \
    && ttyd --help > /tmp/ttyd-help.txt 2>&1 \
    && grep -q -- '--writable' /tmp/ttyd-help.txt \
    && grep -q -- '--check-origin' /tmp/ttyd-help.txt

FROM ${KALI_IMAGE}
LABEL org.opencontainers.image.title="SmartKEA Kali terminal toolbox" \
      org.opencontainers.image.description="Unprivileged isolated teaching tools; no Docker socket or sudo" \
      org.opencontainers.image.vendor="SmartKEA CyberInnovation"
ENV DEBIAN_FRONTEND=noninteractive HOME=/home/learner TERM=xterm-256color \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
COPY --from=ttyd-build /tmp/ttyd-runtime-packages.txt /tmp/ttyd-runtime-packages.txt
RUN apt-get update \
    && xargs -r apt-get install -y --no-install-recommends < /tmp/ttyd-runtime-packages.txt \
    && apt-get install -y --no-install-recommends \
       bash dash coreutils findutils grep sed gawk ripgrep less nano vim-tiny man-db \
       procps iproute2 iputils-ping dnsutils curl wget jq file tar gzip zip unzip \
       openssl ca-certificates git openssh-client netcat-openbsd nmap python3 \
       shellcheck tmux libcap2-bin libwebsockets-evlib-uv \
    && for binary in /usr/lib/nmap/nmap /usr/bin/ping; do \
         test -x "$binary" || exit 1; \
         file_caps=$(getcap "$binary") || exit 1; \
         if [ -n "$file_caps" ]; then setcap -r "$binary" || exit 1; fi; \
         file_caps=$(getcap "$binary") || exit 1; \
         test -z "$file_caps" || exit 1; \
       done \
    && groupadd --gid 10001 learner \
    && useradd --uid 10001 --gid 10001 --create-home --shell /bin/bash learner \
    && install -d -m 0750 -o learner -g learner /workspace /home/learner \
    && install -d -m 0755 /opt/lab/bin /opt/lab/config /opt/lab/fixtures \
    && dpkg-query -W -f='${Package}\t${Version}\n' > /opt/lab/packages.tsv \
    && find /usr/bin /usr/sbin /bin /sbin -xdev -type f \( -perm /4000 -o -perm /2000 \) -exec chmod a-s {} + \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/ttyd-runtime-packages.txt
COPY --from=ttyd-build /usr/local/bin/ttyd /usr/local/bin/ttyd
COPY --from=ttyd-build --chmod=0444 /src/ttyd/LICENSE /usr/share/doc/ttyd/LICENSE
COPY --chmod=0555 scripts/*.sh /opt/lab/bin/
COPY --chmod=0555 scripts/*.py /opt/lab/bin/
COPY --chmod=0444 config/bashrc /opt/lab/config/bashrc
COPY --chmod=0444 fixtures/README.txt /opt/lab/fixtures/README.txt
# Kali's stock Nmap wrapper assumes raw-socket capabilities. This lab uses TCP
# connect scans only; neither file capabilities nor a privileged wrapper is needed.
RUN ln -s /opt/lab/bin/nmap-unprivileged.sh /usr/local/bin/nmap \
    && nmap --version \
    && ttyd --help > /tmp/ttyd-help.txt 2>&1 \
    && grep -q -- '--writable' /tmp/ttyd-help.txt \
    && grep -q -- '--check-origin' /tmp/ttyd-help.txt \
    && rm /tmp/ttyd-help.txt
USER 10001:10001
WORKDIR /workspace
EXPOSE 7681
# No ENTRYPOINT: `docker compose run toolbox curl ...` invokes curl directly.
CMD ["bash", "--noprofile", "--rcfile", "/opt/lab/config/bashrc"]
