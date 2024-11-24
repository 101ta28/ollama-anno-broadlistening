"""Create summaries for the clusters."""

import pandas as pd

from services.llm import request_to_chat_openai


def overview(config):
    dataset = config["output_dir"]
    path = f"outputs/{dataset}/overview.txt"

    takeaways = pd.read_csv(f"outputs/{dataset}/takeaways.csv")
    labels = pd.read_csv(f"outputs/{dataset}/labels.csv")

    prompt = config["overview"]["prompt"]
    model = config["overview"]["model"]

    ids = labels["cluster-id"].to_list()
    takeaways.set_index("cluster-id", inplace=True)
    labels.set_index("cluster-id", inplace=True)

    input = ""
    for i, id in enumerate(ids):
        input += f"# Cluster {i}/{len(ids)}: {labels.loc[id]['label']}\n\n"
        input += takeaways.loc[id]["takeaways"] + "\n\n"

    messages = [{"role": "user", "content": prompt}, {"role": "user", "content": input}]
    response = request_to_chat_openai(messages=messages, model=model)

    with open(path, "w") as file:
        file.write(response)