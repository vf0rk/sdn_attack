import torchattacks
import torch
import torch.nn.functional as F

def evaluate_attack(model, layer_id, test_loader, atk, normalization):
    atk.set_normalization_used(mean = normalization[0], std = normalization[1])
    test_acc = 0
    n = 0
    model.eval()
    model.stop_ic_id = layer_id
    for i, (X, y) in enumerate(test_loader):
        X, y = X.to('cuda'), y.to('cuda')

        if model.use_rpf:
          model.random_rp_matrix()

        X_adv = atk(X, y)  # advtorch

        if model.use_rpf:
          model.random_rp_matrix()

        with torch.no_grad():
            output = model(X_adv)
        test_acc += (output.max(1)[1] == y).sum().item()
        n += y.size(0)

    pgd_acc = test_acc / n
    return pgd_acc
