import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import create_async_engine

from artigraph import ArtifactModel
from artigraph.db import set_engine

# configure what engine artigraph will use
set_engine(create_async_engine("sqlite+aiosqlite:///example.db"), create_tables=True)


# define a model of your data
@dataclass(frozen=True)
class MyData(ArtifactModel, version=1):
    some_value: int
    another_value: dict[str, str]


async def main():
    # construct an artifact
    artifact = MyData(some_value=42, another_value={"foo": "bar"})
    # save it to the database
    artifact_id = await artifact.create(label="my-data")

    # read it back for demonstration purposes
    artifact_from_db = await MyData.read(artifact_id)
    # verify that it's the same as the original
    assert artifact_from_db == artifact


if __name__ == "__main__":
    asyncio.run(main())
