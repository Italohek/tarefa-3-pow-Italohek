import hashlib
import os


def build_merkle_root_and_proof(file_path, target_hex):
    txids_bytes = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # como o exercício fala pra usar os bytes crus, bytes.fromhex() faz isso e mantém o big-endian requisitado
            if line:
                txids_bytes.append(bytes.fromhex(line))

    target_bytes = bytes.fromhex(target_hex)
    
    # garante que o txx que queremos está no bloco
    if target_bytes not in txids_bytes:
        raise ValueError("Target transaction not found in the list.")
    
    # começamos a hashear a árvore pela linha 0, e vamos escalando ela  
    current_level = txids_bytes
    target_index = current_level.index(target_bytes)
    proof = []

    # continuamos combinando as linhas até chegar na raiz da árvore, que vai ter lenght 1
    while len(current_level) > 1:
        next_level = []
        
        # arvore binária, vemos se é pra esquerda ou direita e somamos -1 ou +1 dependendo da direção
        is_right_child = (target_index % 2 == 1)
        sibling_index = target_index - 1 if is_right_child else target_index + 1
        
        # se a linha tiver um número impar, o ultimo item casa com ele mesmo
        if sibling_index < len(current_level):
            proof.append(current_level[sibling_index].hex())
        else:
            proof.append(current_level[target_index].hex())

        # hasha os pares 
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if (i + 1 < len(current_level)) else left
            
            # concatena os bytes crus e usa o single sha256 hash solicitado
            combined = left + right
            level_hash = hashlib.sha256(combined).digest()
            next_level.append(level_hash)
            
        # sobe na árvore e troca a linha antiga com a nova
        current_level = next_level
        target_index = target_index // 2

    merkle_root = current_level[0].hex()
    
    os.makedirs('solutions', exist_ok=True)
    with open('solutions/exercise02.txt', 'w') as f:
        f.write(merkle_root + '\n')
        for p in proof:
            f.write(p + '\n')
            
    return merkle_root, proof

if __name__ == "__main__":
    target_txid = '49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb'
    root, proof = build_merkle_root_and_proof('data/ex02_txid_list.txt', target_txid)
    