# Proposal 11
## Dataset Ownership Verification by Backdoor
Keywords: Backdoor, Dataset Ownership
#### Summary
This project explores how to verify the ownership of a dataset by backdoor. The core idea is
to implant hidden triggers in the training data, causing the model trained on the protected
dataset to produce a pre-defined anomalous response to specific inputs. Data owners can
efficiently verify their ownership without disclosing the original data by observing whether
the third-party model exhibits this specific backdoor behavior.
#### Detailed Description
Background: As deep learning becomes increasingly reliant on high-quality data, pro-
tecting large-scale datasets from unauthorized scraping or training has become a pressing
need in the field of copyright protection. Based on this background and inspired by back-
door attacks, researchers have proposed a new paradigm for verifying dataset ownership
through backdoor mechanisms [7]. Its core logic lies in leveraging the overfitting proper-
ties of neural networks to transform specific trigger patterns into identifiable copyright
signals.

Possible ideas:
- Traditional Backdoor: Traditional backdoor methods based on poisoning (such
as BadNets [5]) implant copyright signals by injecting samples with obvious triggers
(such as specific pixel blocks) and incorrect labels into the training set.
- Stealth Backdoor: using steganography, brightness shifts, or high-frequency
noise to make triggers visually undetectable, thereby improving the concealment of
verification.

Papers:
[7] https://arxiv.org/pdf/2209.06015, [5] https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8685687
Git link to the repository from one of the papers: https://github.com/THUYimingLi/DVBW

Information on the CIFAR-10 dataset: https://www.cs.toronto.edu/~kriz/cifar.html
