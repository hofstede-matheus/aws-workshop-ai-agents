# aws-workshop-ai-agents

## Configurar AWS

- Crie uma policy com essas permissões:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

- Crie um usuário com essa Policy
- Gere uma access key em Users > (usuário) > Security Credentials > Access keys >
  Command Line Interface (CLI)
- Exportar credenciais do usuário

```
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

[Getting Started Oficial](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/amazon-bedrock/#getting-started)

## Como usar

```
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

## Diagramas

```mermaid
architecture-beta
    group sources(cloud)[Sources]
    group agents(server)[Agents]
    group tools(functions)[Tools]
    group storage(database)[Storage]
    group providers(cloud)[Model Provider]

    service youtube(internet)[YouTube video URL] in sources

    service coordinator(server)[Coordinator Agent] in agents

    service yt_dl(functions)[YouTube Downloader Tool] in tools
    service s3_uploader(functions)[S3 Upload Tool] in tools
    service transcriber(functions)[Transcribe Tool] in tools
    service aws_context(functions)[AWS Context Tool] in tools

    service s3_bucket(disk)[S3 Bucket] in storage

    service bedrock(cloud)[Amazon Bedrock Model] in providers

    youtube:R --> L:coordinator
    coordinator:R --> L:yt_dl
    yt_dl:R --> L:s3_uploader
    s3_uploader:R --> L:s3_bucket
    coordinator:R --> L:transcriber
    transcriber:R --> L:s3_bucket
    coordinator:R --> L:aws_context
    coordinator:R --> L:bedrock
```

```mermaid
sequenceDiagram
    participant YT as YouTube
    participant C as Coordinator Agent
    participant YDL as YouTube Downloader Tool
    participant S3U as S3 Upload Tool
    participant S3 as S3 Bucket
    participant TR as Transcribe Tool
    participant BR as Bedrock Model

    YT->>C: YouTube video URL

    C->>YDL: Download audio
    YDL-->>C: audio.mp3 saved locally

    C->>S3U: Upload audio.mp3
    S3U->>S3: PutObject audio.mp3
    S3-->>S3U: Storage confirmation
    S3U-->>C: S3 URI

    C->>TR: Transcribe s3://.../audio.mp3
    TR->>S3: Save transcription
    S3-->>TR: Storage confirmation
    TR-->>C: Transcript ready (S3 URI)

    C->>BR: Generate exam-style questions
    BR-->>C: Questions generated

    C-->>YT: Process complete
```

Links úteis:

- [Agents as Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agents-as-tools/)
