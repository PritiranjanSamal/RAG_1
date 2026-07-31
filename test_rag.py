from rag import pipeline 

response = pipeline.ask("What is the reservation for ST according to Indian Constitution?") 

print("Answer:")
print(response.answer)

print("\nSources:")
for source in response.sources:
    print(source.metadata)