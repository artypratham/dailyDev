"""Seed database with initial topics."""
import asyncio
from sqlalchemy import select
from app.core.database import async_session_maker, init_db
from app.models.topic import Topic


INITIAL_TOPICS = [
    {
        "name": "DSA",
        "slug": "dsa",
        "description": "Master Data Structures and Algorithms with real-world examples from top companies",
        "icon": "🧮",
        "total_concepts": "30",
    },
    {
        "name": "System Design",
        "slug": "system-design",
        "description": "Learn to design scalable systems like Netflix, Twitter, and Uber",
        "icon": "🏗️",
        "total_concepts": "30",
    },
    {
        "name": "LLD",
        "slug": "lld",
        "description": "Low-Level Design patterns and SOLID principles with practical implementations",
        "icon": "📐",
        "total_concepts": "25",
    },
    {
        "name": "Applied AI",
        "slug": "applied-ai",
        "description": "Build production AI systems: RAG pipelines, LLM applications, and ML engineering",
        "icon": "🤖",
        "total_concepts": "25",
    },
    {
        "name": "Computer Networks",
        "slug": "networks",
        "description": "Deep dive into TCP/IP, HTTP, DNS, and networking fundamentals",
        "icon": "🌐",
        "total_concepts": "20",
    },
    {
        "name": "Operating Systems",
        "slug": "os",
        "description": "Understand processes, threads, memory management, and OS internals",
        "icon": "💻",
        "total_concepts": "20",
    },
    {
        "name": "DBMS",
        "slug": "dbms",
        "description": "Database management, SQL optimization, transactions, and indexing",
        "icon": "🗄️",
        "total_concepts": "20",
    },
    {
        "name": "Backend Engineering",
        "slug": "backend",
        "description": "API design, authentication, caching, and backend best practices",
        "icon": "⚙️",
        "total_concepts": "25",
    },
    {
        "name": "Scalability",
        "slug": "scalability",
        "description": "Learn to build systems that handle millions of users",
        "icon": "📈",
        "total_concepts": "20",
    },
    {
        "name": "Distributed Systems",
        "slug": "distributed-systems",
        "description": "Consensus, replication, partitioning, and distributed computing fundamentals",
        "icon": "🔄",
        "total_concepts": "25",
    },
]


async def seed_topics():
    """Seed topics into the database."""
    await init_db()

    async with async_session_maker() as session:
        for topic_data in INITIAL_TOPICS:
            # Check if topic already exists
            result = await session.execute(
                select(Topic).where(Topic.slug == topic_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                topic = Topic(**topic_data)
                session.add(topic)
                print(f"Added topic: {topic_data['name']}")
            else:
                print(f"Topic already exists: {topic_data['name']}")

        await session.commit()
        print("\nSeeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_topics())
