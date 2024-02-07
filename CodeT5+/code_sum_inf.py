from transformers import T5ForConditionalGeneration, AutoTokenizer
import json

checkpoint = "Salesforce/codet5p-220m-bimodal"
model_checkpoint = "./saved_models/summarize_python/checkpoint-78690"  
device = "cpu"  # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = T5ForConditionalGeneration.from_pretrained(model_checkpoint, trust_remote_code=True).to(device)

generate_count = 0

with open('repo_chunks.jsonl', 'r') as f:
    for line in f:
        chunk = json.loads(line)
        code = chunk.get('code_chunk', '')  # assuming 'code' is the key for the code chunk
        # Now you can process the code chunk
        input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)
        if input_ids.shape[1] > 512: # if the code chunk is too long, skip this
            continue
        generated_ids = model.generate(input_ids, max_length=20)
        summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        # append this to the repo_chunks.jsonl file
        chunk['summary'] = summary
        with open('repo_chunks_summary.jsonl', 'a') as f:
            f.write(json.dumps(chunk) + '\n')
        generate_count += 1
        if generate_count % 10 == 0:
            print(f"Generated {generate_count} summaries")
