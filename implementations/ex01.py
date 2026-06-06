import csv
import os

def build_block():
    txs = {}

    filepath = 'data/mempool.csv'
        
    # abre o mempool e guarda tudo no txs da forma que o problema solicida (txid, fee, weight, parents)
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            txid = row[0]
            fee = int(row[1])
            weight = int(row[2])
            parents = row[3].split(';') if len(row) > 3 and row[3] else []
            txs[txid] = {'fee': fee, 'weight': weight, 'parents': parents}

    # calcula toda a linha das transações. basicamente pega a árvore de transações inteira desde o primeiro pai
    def get_ancestors(txid, memo):
        if txid in memo: return memo[txid]
        ancestors = set()
        for p in txs[txid]['parents']:
            ancestors.add(p)
            ancestors.update(get_ancestors(p, memo))
        memo[txid] = ancestors
        return ancestors

    ancestors_memo = {}
    for txid in txs:
        get_ancestors(txid, ancestors_memo)


    MAX_WEIGHT = 4000000
    included = set()
    block = []
    current_weight = 0
    current_fee = 0

    # usa pesquisa em profundidade para o ancestral mais antigo e adiciona primeiro
    def add_tx_and_ancestors(txid):
        nonlocal current_weight, current_fee
        to_add = []
        
        def dfs(t):
            for p in txs[t]['parents']:
                if p not in included and p not in added_in_this_pass:
                    dfs(p)
            added_in_this_pass.add(t)
            to_add.append(t)
            
        added_in_this_pass = set()
        if txid not in included:
            dfs(txid)
            
        # verifica se o peso do pacote não faz o bloco exceder os 4000000, caso não exceda, adiciona e atualiza o peso e a taxa
        pkg_weight = sum(txs[t]['weight'] for t in to_add)
        if current_weight + pkg_weight <= MAX_WEIGHT:
            for t in to_add:
                included.add(t)
                block.append(t)
                current_weight += txs[t]['weight']
                current_fee += txs[t]['fee']
            return True
        return False

    # transação incluida no roteiro
    mandatory_tx = '4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6'
    if mandatory_tx in txs:
        add_tx_and_ancestors(mandatory_tx)
    else:
        print(f"Sem transação obrigatória")

    # maximiza o lucro encontrando a transação com melhor taxa de rentabilidade e adiciona ela, se repetindo até acabar o espaço 
    while True:
        best_tx = None
        best_fee_rate = -1
        
        for txid in txs:
            if txid in included:
                continue
                
            unincluded_anc = ancestors_memo[txid] - included
            pkg_weight = txs[txid]['weight'] + sum(txs[a]['weight'] for a in unincluded_anc)
            
            if current_weight + pkg_weight > MAX_WEIGHT:
                continue
                
            pkg_fee = txs[txid]['fee'] + sum(txs[a]['fee'] for a in unincluded_anc)
            
            fee_rate = pkg_fee / pkg_weight
            if fee_rate > best_fee_rate:
                best_fee_rate = fee_rate
                best_tx = txid
                
        if best_tx is None:
            break
            
        add_tx_and_ancestors(best_tx)
        
    # joga tudo no arquivo de solutions/exercise01.txt
    os.makedirs('solutions', exist_ok=True)
    with open('solutions/exercise01.txt', 'w') as f:
        for t in block:
            f.write(t + '\n')


if __name__ == "__main__":
    build_block()