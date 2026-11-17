import os


class BinaryEngine:

  @staticmethod
  def compare_files(path1, path2):
    with open(path1, "rb") as f1, open(path2, "rb") as f2:
      data1 = f1.read()
      data2 = f2.read()

    if len(data1) != len(data2):
      raise ValueError(
          f"Size mismatch: File 1 is {len(data1)} bytes, File 2 is"
          f" {len(data2)} bytes."
      )

    differences = []
    for i in range(len(data1)):
      if data1[i] != data2[i]:
        differences.append((i, data1[i], data2[i]))

    return data1, data2, differences

  @staticmethod
  def compute_contiguous_blocks(diff_list):
    if not diff_list:
      return []
    blocks = []
    start_addr = diff_list[0][0]
    prev_addr = start_addr

    for item in diff_list[1:]:
      addr = item[0]
      if addr == prev_addr + 1:
        prev_addr = addr
      else:
        blocks.append((start_addr, prev_addr, (prev_addr - start_addr + 1)))
        start_addr = addr
        prev_addr = addr
    blocks.append((start_addr, prev_addr, (prev_addr - start_addr + 1)))
    return blocks

  @staticmethod
  def search_pattern(file_path, query, search_type):
    with open(file_path, "rb") as f:
      file_data = f.read()

    if search_type == "Hex":
      clean_q = query.replace("0x", "").replace(" ", "")
      search_bytes = bytes.fromhex(clean_q)
    else:
      search_bytes = query.encode("ascii")

    matches = []
    pos = 0
    while True:
      pos = file_data.find(search_bytes, pos)
      if pos == -1:
        break
      matches.append(pos)
      pos += 1
    return matches, search_bytes