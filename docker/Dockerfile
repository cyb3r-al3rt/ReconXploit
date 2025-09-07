# ReconXploit v3.0 - Docker Image
# Product of Kernelpanic under infosbios.tech
FROM kalilinux/kali-rolling:latest

LABEL maintainer="cyb3r-ssrf"
LABEL version="3.0.0"
LABEL description="ReconXploit - Advanced Reconnaissance Automation Framework"
LABEL organization="Kernelpanic"
LABEL website="infosbios.tech"

ENV DEBIAN_FRONTEND=noninteractive
ENV GOPATH=/opt/go
ENV PATH=$PATH:/opt/go/bin:/usr/local/go/bin
ENV RECONXPLOIT_HOME=/opt/reconxploit
ENV PYTHONPATH=$RECONXPLOIT_HOME

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y \
        python3 python3-pip python3-venv python3-dev \
        git curl wget unzip jq parallel \
        build-essential libssl-dev libffi-dev \
        chromium firefox-esr \
        dnsutils whois nmap masscan \
        gobuster dirb nikto sqlmap \
        ca-certificates apt-transport-https \
        software-properties-common && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    wget -q https://golang.org/dl/go1.21.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz && \
    rm go1.21.0.linux-amd64.tar.gz

RUN useradd -m -s /bin/bash -u 1000 reconxploit && \
    mkdir -p $RECONXPLOIT_HOME && \
    chown -R reconxploit:reconxploit $RECONXPLOIT_HOME

USER reconxploit
WORKDIR $RECONXPLOIT_HOME

RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest && \
    go install github.com/projectdiscovery/katana/cmd/katana@latest && \
    go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest && \
    go install github.com/tomnomnom/assetfinder@latest && \
    go install github.com/tomnomnom/gf@latest && \
    go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/lc/gau/v2/cmd/gau@latest && \
    go install github.com/ffuf/ffuf@latest && \
    go install github.com/epi052/feroxbuster@latest && \
    go install github.com/hakluke/hakrawler@latest

COPY --chown=reconxploit:reconxploit . $RECONXPLOIT_HOME/

RUN python3 -m venv $RECONXPLOIT_HOME/venv && \
    . $RECONXPLOIT_HOME/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

RUN mkdir -p $RECONXPLOIT_HOME/wordlists && \
    git clone --depth 1 https://github.com/danielmiessler/SecLists.git $RECONXPLOIT_HOME/wordlists/SecLists && \
    git clone --depth 1 https://github.com/swisskyrepo/PayloadsAllTheThings.git $RECONXPLOIT_HOME/wordlists/PayloadsAllTheThings

RUN mkdir -p $RECONXPLOIT_HOME/results $RECONXPLOIT_HOME/logs

RUN $GOPATH/bin/nuclei -update-templates

RUN chmod +x $RECONXPLOIT_HOME/docker/entrypoint.sh

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["--help"]
