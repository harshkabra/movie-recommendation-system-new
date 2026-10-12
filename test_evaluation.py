from src.evaluation import evaluate_precision_recall


print("========================================")
print("Hybrid Weight Experiment")
print("========================================")


print("\n--- 60% User + 40% Content ---")

evaluate_precision_recall(
    number_of_users=20,
    k=10,
    user_weight=0.6,
    content_weight=0.4
)


print("\n--- 70% User + 30% Content ---")

evaluate_precision_recall(
    number_of_users=20,
    k=10,
    user_weight=0.7,
    content_weight=0.3
)


print("\n--- 80% User + 20% Content ---")

evaluate_precision_recall(
    number_of_users=20,
    k=10,
    user_weight=0.8,
    content_weight=0.2
)