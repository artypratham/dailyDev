import json
from typing import Dict, Any, Optional
from groq import Groq
from loguru import logger
from app.core.config import settings


class LLMService:
    """Service for LLM-powered content generation using Groq."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.1-70b-versatile"  # Free, fast, capable

    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume and extract skills, experience level, etc."""
        prompt = f"""Analyze this resume and extract structured information.

Resume:
{resume_text}

Return a JSON object with these fields:
- skills: array of technical skills found
- experience_level: "beginner" (0-2 years), "intermediate" (2-5 years), or "advanced" (5+ years)
- strengths: array of 3-5 key strengths
- weaknesses: array of areas that need improvement for interviews
- recommended_topics: array of topics to focus on (from: DSA, System Design, LLD, Applied AI, Networks, OS, DBMS, Backend, Scalability, Distributed Systems)
- years_of_experience: estimated years
- tech_stack: array of technologies/frameworks

Return ONLY valid JSON, no explanations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
            )
            result = response.choices[0].message.content
            # Parse JSON from response
            return json.loads(result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return self._default_skill_analysis()
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return self._default_skill_analysis()

    def _default_skill_analysis(self) -> Dict[str, Any]:
        """Return default skill analysis when LLM fails."""
        return {
            "skills": [],
            "experience_level": "beginner",
            "strengths": [],
            "weaknesses": ["Unable to analyze resume"],
            "recommended_topics": ["DSA", "System Design"],
            "years_of_experience": 0,
            "tech_stack": [],
        }

    async def generate_hook_message(
        self,
        topic_name: str,
        concept_name: str,
        difficulty: str,
        user_experience_level: str = "intermediate"
    ) -> str:
        """Generate an engaging WhatsApp hook message."""
        prompt = f"""You are a senior software engineer writing engaging interview prep content.

Topic: {topic_name}
Concept: {concept_name}
Difficulty: {difficulty}
User Level: {user_experience_level}

Write a WhatsApp hook message (50-150 words) that:
1. Starts with a real-world problem from companies like Netflix, Google, Amazon, Uber, etc.
2. Creates curiosity by hinting at the CS concept that solves it
3. Ends with asking if they want to learn more
4. Uses ONE emoji for engagement
5. Is conversational, not academic

Format:
"🚀 Real-World Problem:
[Specific scenario from a company]
This is the [CS Concept] problem.
Want to learn how top companies solve this? Reply 'YES' 🎯"

Generate the hook message (just the message, no explanations):"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Hook message generation failed: {e}")
            return f"🎯 Today's concept: {concept_name}\n\nWant to learn about this? Reply 'YES'"

    async def generate_article(
        self,
        topic_name: str,
        concept_name: str,
        user_skill_summary: Optional[str] = None,
        language: str = "Python"
    ) -> Dict[str, Any]:
        """Generate a comprehensive article for a concept."""
        prompt = f"""You are an expert software engineer writing educational content.

Topic: {topic_name}
Concept: {concept_name}
User Background: {user_skill_summary or "Intermediate developer preparing for interviews"}

Create a comprehensive article with these sections:

1. ELI5 (Explain Like I'm 5):
   - Use simple analogies (pizza delivery, library system, traffic)
   - 2-3 paragraphs max
   - No technical jargon

2. Technical Deep Dive:
   - Detailed explanation with proper terminology
   - Why this approach works
   - Trade-offs and alternatives
   - Complexity analysis (for DSA: time/space)
   - Real architectural implications

3. Code Implementation:
   - Production-quality code in {language}
   - Comments for complex logic
   - Show brute force AND optimized approach if applicable

4. Real-World Examples:
   - How companies use this (Netflix, Google, Amazon, etc.)
   - Production scenarios
   - Edge cases to consider

5. Practice Problems:
   - 2-3 related interview questions
   - Include LeetCode problem names if applicable

Return as JSON:
{{
  "eli5": "...",
  "technical": "...",
  "code_snippets": [{{"language": "{language}", "code": "...", "explanation": "..."}}],
  "real_world": "...",
  "practice": [{{"question": "...", "difficulty": "easy/medium/hard", "link": "optional leetcode url"}}]
}}

Return ONLY valid JSON:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=4000,
            )
            result = response.choices[0].message.content
            # Clean up potential markdown formatting
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            return json.loads(result.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse article JSON: {e}")
            return self._default_article(concept_name)
        except Exception as e:
            logger.error(f"Article generation failed: {e}")
            return self._default_article(concept_name)

    def _default_article(self, concept_name: str) -> Dict[str, Any]:
        """Return default article when generation fails."""
        return {
            "eli5": f"We're working on the explanation for {concept_name}. Check back soon!",
            "technical": "Content is being generated...",
            "code_snippets": [],
            "real_world": "Examples coming soon...",
            "practice": [],
        }

    async def generate_roadmap(
        self,
        topic_name: str,
        duration_days: int,
        user_level: str = "intermediate"
    ) -> list:
        """Generate a personalized learning roadmap for a topic."""
        prompt = f"""Create a {duration_days}-day learning roadmap for {topic_name}.
User Level: {user_level}

The roadmap should:
1. Progress from fundamentals to advanced concepts
2. Each day covers ONE focused concept
3. Mix theoretical and practical concepts
4. Include real-world applications

Return a JSON array of concepts:
[
  {{"day": 1, "concept": "Concept Name", "difficulty": "easy/medium/hard", "read_time": 10}},
  ...
]

For {topic_name}, include foundational concepts first, then build to complex ones.
Return ONLY the JSON array:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=2000,
            )
            result = response.choices[0].message.content
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            return json.loads(result.strip())
        except Exception as e:
            logger.error(f"Roadmap generation failed: {e}")
            return self._default_roadmap(topic_name, duration_days)

    def _default_roadmap(self, topic_name: str, duration_days: int) -> list:
        """Return a default roadmap when generation fails."""
        # Fallback roadmaps for common topics
        default_concepts = {
            "DSA": [
                "Arrays and Basic Operations",
                "Two Pointers Technique",
                "Sliding Window",
                "Hash Maps and Sets",
                "Binary Search",
                "Linked Lists",
                "Stacks",
                "Queues",
                "Trees - Binary Trees",
                "Binary Search Trees",
                "Tree Traversals (BFS/DFS)",
                "Heaps and Priority Queues",
                "Graphs - Representation",
                "Graph BFS",
                "Graph DFS",
                "Dijkstra's Algorithm",
                "Dynamic Programming - Basics",
                "DP - Memoization",
                "DP - Tabulation",
                "Backtracking",
                "Greedy Algorithms",
                "Sorting Algorithms",
                "Merge Sort",
                "Quick Sort",
                "Trie Data Structure",
                "Union Find",
                "Segment Trees",
                "Bit Manipulation",
                "String Algorithms",
                "Advanced Problem Solving",
            ],
            "System Design": [
                "System Design Basics",
                "Scalability Fundamentals",
                "Load Balancing",
                "Caching Strategies",
                "Database Sharding",
                "CAP Theorem",
                "Consistent Hashing",
                "Message Queues",
                "Microservices Architecture",
                "API Design",
                "Rate Limiting",
                "CDN and Edge Computing",
                "Database Replication",
                "SQL vs NoSQL",
                "Distributed Systems Basics",
                "Consensus Algorithms",
                "Event-Driven Architecture",
                "Real-time Systems",
                "Search Systems",
                "Notification Systems",
                "URL Shortener Design",
                "Twitter/Feed Design",
                "Chat Application Design",
                "Video Streaming Design",
                "E-commerce Design",
                "Ride-sharing Design",
                "Payment Systems",
                "Monitoring and Logging",
                "Security Best Practices",
                "System Design Interview Tips",
            ],
        }

        concepts = default_concepts.get(topic_name, default_concepts["DSA"])
        roadmap = []
        for i in range(min(duration_days, len(concepts))):
            difficulty = "easy" if i < duration_days // 3 else ("medium" if i < 2 * duration_days // 3 else "hard")
            roadmap.append({
                "day": i + 1,
                "concept": concepts[i],
                "difficulty": difficulty,
                "read_time": 10 + (i % 5) * 2,
            })
        return roadmap


# Singleton instance
llm_service = LLMService()
