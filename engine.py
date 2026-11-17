import os
from typing import Callable, Dict, List, Optional, Tuple


def compare_binaries(
    file1_path: str,
    file2_path: str,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> Dict:
  """
    Compare deux fichiers binaires octet par octet avec suivi de progression.
    Retourne les statistiques complètes et la liste des blocs modifiés.
    """
  size1 = os.path.getsize(file1_path)
  size2 = os.path.getsize(file2_path)

  with open(file1_path, "rb") as f1:
    data1 = f1.read()
  with open(file2_path, "rb") as f2:
    data2 = f2.read()

  min_len = min(size1, size2)
  max_len = max(size1, size2)

  mv1 = memoryview(data1)
  mv2 = memoryview(data2)

  blocks: List[Tuple[int, int]] = []
  diff_bytes_count = 0
  in_block = False
  start_offset = 0

  # Notifier tous les 1 % pour éviter de saturer le signal Qt
  step = max(1, min_len // 100)

  for i in range(min_len):
    if mv1[i] != mv2[i]:
      diff_bytes_count += 1
      if not in_block:
        start_offset = i
        in_block = True
    else:
      if in_block:
        blocks.append((start_offset, i - 1))
        in_block = False

    if progress_callback and (i % step == 0):
      percent = int((i / min_len) * 100)
      progress_callback(percent)

  if in_block:
    blocks.append((start_offset, min_len - 1))

  # Si les fichiers n'ont pas la même taille, compter l'excédent comme différence
  if size1 != size2:
    diff_bytes_count += max_len - min_len
    blocks.append((min_len, max_len - 1))

  if progress_callback:
    progress_callback(100)

  similarity = (
      100.0
      if max_len == 0
      else max(0.0, ((max_len - diff_bytes_count) / max_len) * 100.0)
  )

  return {
      "size1": size1,
      "size2": size2,
      "diff_bytes": diff_bytes_count,
      "total_blocks": len(blocks),
      "similarity": similarity,
      "blocks": blocks,
      "data1": data1,
      "data2": data2,
  } 