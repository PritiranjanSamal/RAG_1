from rag import pipeline 
response = pipeline.ask("What is the minimum age to become a rajya sabha member in India?") 

print("Answer:")
print(response.answer)

print("\nSources:")
for source in response.sources:
    print(source.metadata)
