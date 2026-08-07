from rag import pipeline 
response = pipeline.ask("In which year was the constitution was adopted?") 

print("Answer:")
print(response.answer)

print("\nSources:")
for source in response.sources:
    print(source.metadata)










# # Force reload to pick up changes
# import sys
# if 'rag' in sys.modules:
#     del sys.modules['rag']
# if 'core.retriever' in sys.modules:
#     del sys.modules['core.retriever']
# if 'core.query_preprocessor' in sys.modules:
#     del sys.modules['core.query_preprocessor']

# from rag import pipeline 

# print("\n" + "="*70)
# print("RAG Pipeline with Query Preprocessing - Testing")
# print("="*70)

# # Test with your original problematic query
# original_query = "In which year was the new constitution was drafted?"

# print(f"\n🔍 Original Query: {original_query}")
# print("\n⏳ Processing with query expansion...\n")

# response = pipeline.ask(original_query)

# print("\n" + "="*70)
# print("📊 RESULTS")
# print("="*70)

# print("\n✅ Answer:")
# print(response.answer)

# print("\n📚 Top 5 Sources:")
# for i, source in enumerate(response.sources[:5], 1):
#     file_name = source.metadata.get('source_file', 'Unknown')
#     page = source.metadata.get('page', '?')
#     score = source.score
    
#     # Highlight if it's the main constitution document
#     marker = "⭐" if "Constitution Of India.pdf" in file_name else "  "
    
#     print(f"{marker} {i}. {file_name} (page {page}) - Score: {score:.3f}")

# print("\n" + "="*70)

# # Test a few more challenging queries
# print("\n\n🔬 Additional Test Queries:\n")

# test_queries = [
#     "When was India's constitution written?",
#     "Constitution drafting year",
#     "What year was the constitution made?"
# ]

# for query in test_queries:
#     print(f"\n❓ Query: {query}")
#     response = pipeline.ask(query)
#     print(f"💬 Answer: {response.answer[:150]}...")  # First 150 chars
#     print(f"📄 Best source: {response.sources[0].metadata.get('source_file', 'Unknown')} (score: {response.sources[0].score:.3f})")
