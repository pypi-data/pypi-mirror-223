## Chroma Migrate

Schema and data format changes are a necessary evil of evolving software. We take changes seriously and make them infrequently and only when necessary.

Chroma's commitment is whenever schema or data format change, we will provide a seamless and easy-to-use migration tool to move to the new schema/format. 

Specifically we will announce schema changes on:
- Discord ([#migrations channel](https://discord.com/channels/1073293645303795742/1129286514845691975))
- Github (here)
- Email listserv [Sign up](https://airtable.com/shrHaErIs1j9F97BE)

We will aim to provide:
- a description of the change and the rationale for the change.
- a CLI migration tool you can run
- a video walkthrough of using the tool

### Migration Log

#### Migration from >0.4.0 to 0.4.0 - July 17, 2023

We are migrating:
- `metadata store`: where metadata is stored
- `index on disk`: how indexes are stored on disk

`Metadata Store`: Previously Chroma used underlying storage engines `DuckDB` for the `in-memory` version of Chroma, and `Clickhouse` for the `single-node server` version of Chroma. These decisions were made when Chroma was addressing more batch analytical workloads and are no longer the best choice for users. The new metadata store for the `in-memory` and `single-node server` version of Chroma will be `sqlite`. (The distributed version of Chroma (forthcoming), will use a different distributed metadata store.)

`Index store`: Previously Chroma saved the **entire** index on every write. This because painfully slow when the collection grew to a reasonable amount of embeddings. The new index store saves *only the change* and should scale seamlessly! 

Here are the 9-possible migration paths, and any notes, if applicable.

| From 👇&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;➡️&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To 👉 | Persistent Chroma | Local Chroma Server | Remote Chroma Server |
| -------- | -------- | -------- | -------- |
| Persistent Chroma | ✅ | ✅ | 1️⃣ |
| Local Chroma Server| ✅| 2️⃣| 1️⃣|
| Remote Chroma Server| ✅| ✅| 1️⃣ 2️⃣|

1️⃣ - Make sure to configure any auth headers correctly

2️⃣ - Run both the existing version of Chroma and the new `0.4.0` version of Chroma at same time. Run the new version on a new port if local.

[Embed video here]()

##### How to use the migration tool

1. `pip` install this utility. `pip install chroma_migrate`

1. Running the CLI. In your terminal run:

```
chroma_migrate
```

2. Choose whether the data you want to migrate is locally on disk (duckdb) on  clickhouse instance used by chroma, or directly from another chroma server

3. Choose where you want to write the new data to. 

### Developing Locally
Run python main.py to test locally
