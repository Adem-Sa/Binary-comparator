import os
import sys
from engine import compare_binaries
from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPen,
    QPixmap,
    QSyntaxHighlighter,
    QTextCharFormat,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


TRANSLATIONS = {
    "EN": {
        "file1_label": "File 1 (Original):",
        "file1_placeholder": "Select the first .bin file...",
        "file2_label": "File 2 (Modified):",
        "file2_placeholder": "Select the second .bin file...",
        "browse": "Browse...",
        "compare": "Compare Files",
        "export": "Export (.txt)",
        "clear": "Clear",
        "progress_scan": "Binary analysis: %p%",
        "progress_render": "Loading blocks: {loaded:,} / {total:,}",
        "stat_file1": "File 1:",
        "stat_file2": "File 2:",
        "stat_diffs": "Different bytes:",
        "stat_blocks": "Modified blocks:",
        "stat_sim": "Similarity:",
        "hex_header1": "HEXADECIMAL PREVIEW — FILE 1 (ORIGINAL)",
        "hex_header2": "HEXADECIMAL PREVIEW — FILE 2 (MODIFIED)",
        "select_dialog": "Select File {index}",
        "file_filter": (
            "Binary files (*.bin *.ori *.mod *.hex *.eep *.mpc *.fls);;All"
            " files (*.*)"
        ),
        "warn_missing_title": "Missing Files",
        "warn_missing_msg": "Please select both files before comparing.",
        "err_title": "Error",
        "err_not_found": "One of the selected files could not be found.",
        "err_analysis_title": "Analysis Error",
        "identical_msg": "Both files are strictly identical.",
        "block_header": (
            "=== BLOCK #{idx:03d} | Offset: 0x{start:08X} -> 0x{end:08X}"
            " ({count} bytes) ==="
        ),
        "export_dialog": "Save Full Comparison Report",
        "export_filter": "Text file (*.txt);;All files (*.*)",
        "export_success_title": "Export Successful",
        "export_success_msg": (
            "The full report ({total:,} blocks) has been saved to:\n{path}"
        ),
        "export_err_title": "Export Error",
        "report_title": "FULL BINARY COMPARISON REPORT",
        "report_orig": "ORIGINAL (File 1)",
        "report_mod": "MODIFIED (File 2)",
    },
    "FR": {
        "file1_label": "File 1 (Original) :",
        "file1_placeholder": "Sélectionner le premier fichier .bin...",
        "file2_label": "File 2 (Modifié) :",
        "file2_placeholder": "Sélectionner le second fichier .bin...",
        "browse": "Parcourir...",
        "compare": "Comparer les fichiers",
        "export": "Exporter (.txt)",
        "clear": "Effacer",
        "progress_scan": "Analyse binaire : %p%",
        "progress_render": "Chargement des blocs : {loaded:,} / {total:,}",
        "stat_file1": "File 1 :",
        "stat_file2": "File 2 :",
        "stat_diffs": "Octets différents :",
        "stat_blocks": "Blocs modifiés :",
        "stat_sim": "Similarité :",
        "hex_header1": "APERÇU HEXADÉCIMAL — FILE 1 (ORIGINAL)",
        "hex_header2": "APERÇU HEXADÉCIMAL — FILE 2 (MODIFIÉ)",
        "select_dialog": "Sélectionner File {index}",
        "file_filter": (
            "Fichiers binaires (*.bin *.ori *.mod *.hex *.eep *.mpc"
            " *.fls);;Tous les fichiers (*.*)"
        ),
        "warn_missing_title": "Fichiers manquants",
        "warn_missing_msg": "Veuillez sélectionner les deux fichiers.",
        "err_title": "Erreur",
        "err_not_found": "Un des fichiers sélectionnés est introuvable.",
        "err_analysis_title": "Erreur d'analyse",
        "identical_msg": "Les deux fichiers sont strictement identiques.",
        "block_header": (
            "=== BLOC #{idx:03d} | Offset: 0x{start:08X} -> 0x{end:08X}"
            " ({count} octets) ==="
        ),
        "export_dialog": "Enregistrer le rapport complet",
        "export_filter": "Fichier texte (*.txt);;Tous les fichiers (*.*)",
        "export_success_title": "Export réussi",
        "export_success_msg": (
            "Le rapport complet ({total:,} blocs) a été enregistré :\n{path}"
        ),
        "export_err_title": "Erreur d'export",
        "report_title": "RAPPORT COMPLET DE COMPARAISON BINAIRE",
        "report_orig": "ORIGINAL (File 1)",
        "report_mod": "MODIFIÉ  (File 2)",
    },
    "AR": {
        "file1_label": "الملف 1 (الأصلي):",
        "file1_placeholder": "اختر ملف .bin الأول...",
        "file2_label": "الملف 2 (المعدّل):",
        "file2_placeholder": "اختر ملف .bin الثاني...",
        "browse": "استعراض...",
        "compare": "مقارنة الملفات",
        "export": "تصدير (.txt)",
        "clear": "مسح",
        "progress_scan": "جاري التحليل الثنائي: %p%",
        "progress_render": "تحميل الكتل: {loaded:,} / {total:,}",
        "stat_file1": "الملف 1:",
        "stat_file2": "الملف 2:",
        "stat_diffs": "البايتات المختلفة:",
        "stat_blocks": "الكتل المعدّلة:",
        "stat_sim": "نسبة التطابق:",
        "hex_header1": "المعاينة السداسية عشرية — الملف 1 (الأصلي)",
        "hex_header2": "المعاينة السداسية عشرية — الملف 2 (المعدّل)",
        "select_dialog": "اختر الملف {index}",
        "file_filter": (
            "ملفات ثنائية (*.bin *.ori *.mod *.hex *.eep *.mpc *.fls);;جميع"
            " الملفات (*.*)"
        ),
        "warn_missing_title": "ملفات مفقودة",
        "warn_missing_msg": "يرجى اختيار كلا الملفين قبل بدء المقارنة.",
        "err_title": "خطأ",
        "err_not_found": "تعذر العثور على أحد الملفات المحددة.",
        "err_analysis_title": "خطأ في التحليل",
        "identical_msg": "الملفان متطابقان تماماً.",
        "block_header": (
            "=== BLOCK #{idx:03d} | Offset: 0x{start:08X} -> 0x{end:08X}"
            " ({count} bytes) ==="
        ),
        "export_dialog": "حفظ التقرير الكامل",
        "export_filter": "ملف نصي (*.txt);;جميع الملفات (*.*)",
        "export_success_title": "تم التصدير بنجاح",
        "export_success_msg": "تم حفظ التقرير الكامل ({total:,} كتلة) في:\n{path}",
        "export_err_title": "خطأ في التصدير",
        "report_title": "تقرير المقارنة الثنائية الكامل",
        "report_orig": "ORIGINAL (File 1)",
        "report_mod": "MODIFIED (File 2)",
    },
    "RU": {
        "file1_label": "Файл 1 (Оригинал):",
        "file1_placeholder": "Выберите первый файл .bin...",
        "file2_label": "Файл 2 (Изменён):",
        "file2_placeholder": "Выберите второй файл .bin...",
        "browse": "Обзор...",
        "compare": "Сравнить файлы",
        "export": "Экспорт (.txt)",
        "clear": "Очистить",
        "progress_scan": "Бинарный анализ: %p%",
        "progress_render": "Загрузка блоков: {loaded:,} / {total:,}",
        "stat_file1": "Файл 1:",
        "stat_file2": "Файл 2:",
        "stat_diffs": "Различных байт:",
        "stat_blocks": "Изменённых блоков:",
        "stat_sim": "Схожесть:",
        "hex_header1": "HEX-ПРОСМОТР — ФАЙЛ 1 (ОРИГИНАЛ)",
        "hex_header2": "HEX-ПРОСМОТР — ФАЙЛ 2 (ИЗМЕНЁН)",
        "select_dialog": "Выберите файл {index}",
        "file_filter": (
            "Бинарные файлы (*.bin *.ori *.mod *.hex *.eep *.mpc *.fls);;Все"
            " файлы (*.*)"
        ),
        "warn_missing_title": "Файлы не выбраны",
        "warn_missing_msg": "Пожалуйста, выберите оба файла перед сравнением.",
        "err_title": "Ошибка",
        "err_not_found": "Один из выбранных файлов не найден.",
        "err_analysis_title": "Ошибка анализа",
        "identical_msg": "Оба файла полностью идентичны.",
        "block_header": (
            "=== БЛОК #{idx:03d} | Смещение: 0x{start:08X} -> 0x{end:08X}"
            " ({count} байт) ==="
        ),
        "export_dialog": "Сохранить полный отчёт",
        "export_filter": "Текстовый файл (*.txt);;Все файлы (*.*)",
        "export_success_title": "Экспорт выполнен",
        "export_success_msg": (
            "Полный отчёт ({total:,} блоков) успешно сохранён:\n{path}"
        ),
        "export_err_title": "Ошибка экспорта",
        "report_title": "ПОЛНЫЙ ОТЧЁТ БИНАРНОГО СРАВНЕНИЯ",
        "report_orig": "ORIGINAL (File 1)",
        "report_mod": "MODIFIED (File 2)",
    },
    "ZH": {
        "file1_label": "文件 1 (原始):",
        "file1_placeholder": "选择第一个 .bin 文件...",
        "file2_label": "文件 2 (修改):",
        "file2_placeholder": "选择第二个 .bin 文件...",
        "browse": "浏览...",
        "compare": "开始对比",
        "export": "导出 (.txt)",
        "clear": "清空",
        "progress_scan": "二进制分析中: %p%",
        "progress_render": "正在加载数据块: {loaded:,} / {total:,}",
        "stat_file1": "文件 1:",
        "stat_file2": "文件 2:",
        "stat_diffs": "差异字节数:",
        "stat_blocks": "修改数据块:",
        "stat_sim": "相似度:",
        "hex_header1": "十六进制预览 — 文件 1 (原始)",
        "hex_header2": "十六进制预览 — 文件 2 (修改)",
        "select_dialog": "选择文件 {index}",
        "file_filter": (
            "二进制文件 (*.bin *.ori *.mod *.hex *.eep *.mpc *.fls);;所有文件"
            " (*.*)"
        ),
        "warn_missing_title": "缺少文件",
        "warn_missing_msg": "对比前请先选择两个文件。",
        "err_title": "错误",
        "err_not_found": "找不到所选的其中一个文件。",
        "err_analysis_title": "分析错误",
        "identical_msg": "两个文件完全一致。",
        "block_header": (
            "=== 数据块 #{idx:03d} | 偏移量: 0x{start:08X} -> 0x{end:08X}"
            " ({count} 字节) ==="
        ),
        "export_dialog": "保存完整对比报告",
        "export_filter": "文本文件 (*.txt);;所有文件 (*.*)",
        "export_success_title": "导出成功",
        "export_success_msg": "完整报告（共 {total:,} 个数据块）已保存至:\n{path}",
        "export_err_title": "导出错误",
        "report_title": "二进制文件完整对比报告",
        "report_orig": "ORIGINAL (File 1)",
        "report_mod": "MODIFIED (File 2)",
    },
}


class HexDiffHighlighter(QSyntaxHighlighter):
  """Colore uniquement les octets modifiés sans ralentir QPlainTextEdit."""

  def __init__(self, document, is_modified_side: bool = False):
    super().__init__(document)
    self.data1 = b""
    self.data2 = b""

    self.header_format = QTextCharFormat()
    self.header_format.setForeground(QColor("#569cd6"))
    self.header_format.setFontWeight(QFont.Weight.Bold)

    self.offset_format = QTextCharFormat()
    self.offset_format.setForeground(QColor("#808080"))

    self.diff_format = QTextCharFormat()
    self.diff_format.setFontWeight(QFont.Weight.Bold)
    if is_modified_side:
      self.diff_format.setForeground(QColor("#4ec9b0"))
      self.diff_format.setBackground(QColor("#1e3a34"))
    else:
      self.diff_format.setForeground(QColor("#f48771"))
      self.diff_format.setBackground(QColor("#3d2220"))

  def set_binaries(self, data1: bytes, data2: bytes):
    self.data1 = data1
    self.data2 = data2

  def highlightBlock(self, text: str):
    if not text:
      return

    if text.startswith("==="):
      self.setFormat(0, len(text), self.header_format)
      return

    if len(text) >= 11 and text[8:11] == " | ":
      self.setFormat(0, 8, self.offset_format)

      if not self.data1 and not self.data2:
        return

      try:
        row_offset = int(text[:8], 16)
      except ValueError:
        return

      len1 = len(self.data1)
      len2 = len(self.data2)

      for b_idx in range(16):
        abs_offset = row_offset + b_idx
        has1 = abs_offset < len1
        has2 = abs_offset < len2

        if not has1 and not has2:
          break

        is_diff = (has1 != has2) or (
            self.data1[abs_offset] != self.data2[abs_offset]
        )
        if is_diff:
          char_pos = 11 + (b_idx * 3)
          if char_pos + 2 <= len(text):
            self.setFormat(char_pos, 2, self.diff_format)


def resource_path(relative_path: str) -> str:
  base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
  return os.path.join(base_path, relative_path)


def create_globe_icon(color_hex: str = "#4ec9b0") -> QIcon:
  pixmap = QPixmap(16, 16)
  pixmap.fill(Qt.GlobalColor.transparent)
  painter = QPainter(pixmap)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(QColor(color_hex), 1.4)
  painter.setPen(pen)
  painter.drawEllipse(2, 2, 12, 12)
  painter.drawEllipse(5, 2, 6, 12)
  painter.drawLine(2, 8, 14, 8)
  painter.end()
  return QIcon(pixmap)


def format_size(num_bytes: int) -> str:
  if num_bytes < 1024:
    return f"{num_bytes} B"
  elif num_bytes < 1024 * 1024:
    return f"{num_bytes / 1024:.2f} KB ({num_bytes:,} B)"
  else:
    return f"{num_bytes / (1024 * 1024):.2f} MB ({num_bytes:,} B)"


class CompareWorker(QThread):
  progress = pyqtSignal(int)
  finished = pyqtSignal(dict)
  error = pyqtSignal(str)

  def __init__(self, path1: str, path2: str):
    super().__init__()
    self.path1 = path1
    self.path2 = path2

  def run(self):
    try:
      result = compare_binaries(
          self.path1, self.path2, progress_callback=self.progress.emit
      )
      result["path1"] = self.path1
      result["path2"] = self.path2
      self.finished.emit(result)
    except Exception as exc:
      self.error.emit(str(exc))


class BinaryComparatorWindow(QMainWindow):
  BATCH_SIZE = 400

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Binary Comparator")
    self.resize(1200, 780)

    icon_path = resource_path("app_icon.png")
    if os.path.exists(icon_path):
      self.setWindowIcon(QIcon(icon_path))

    # Langue par défaut : Anglais (EN)
    self.current_lang = "EN"
    self.last_result = None
    self.worker = None
    self.render_index = 0

    self.render_timer = QTimer(self)
    self.render_timer.setInterval(15)
    self.render_timer.timeout.connect(self._render_next_batch)

    self._setup_ui()
    self._load_stylesheet()
    self._apply_language()

  def _t(self, key: str) -> str:
    return TRANSLATIONS[self.current_lang][key]

  def _load_stylesheet(self):
    qss_path = resource_path("style.qss")
    if os.path.exists(qss_path):
      with open(qss_path, "r", encoding="utf-8") as f:
        self.setStyleSheet(f.read())

  def _setup_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    main_layout.setSpacing(12)
    main_layout.setContentsMargins(16, 16, 16, 16)

    # --- Sélection des fichiers ---
    file_panel = QFrame()
    file_panel.setObjectName("panel")
    file_layout = QVBoxLayout(file_panel)

    row1 = QHBoxLayout()
    self.lbl1 = QLabel()
    self.lbl1.setFixedWidth(135)
    self.input_file1 = QLineEdit()
    self.input_file1.setReadOnly(True)
    self.btn_browse1 = QPushButton()
    self.btn_browse1.clicked.connect(lambda: self._select_file(1))
    row1.addWidget(self.lbl1)
    row1.addWidget(self.input_file1)
    row1.addWidget(self.btn_browse1)

    row2 = QHBoxLayout()
    self.lbl2 = QLabel()
    self.lbl2.setFixedWidth(135)
    self.input_file2 = QLineEdit()
    self.input_file2.setReadOnly(True)
    self.btn_browse2 = QPushButton()
    self.btn_browse2.clicked.connect(lambda: self._select_file(2))
    row2.addWidget(self.lbl2)
    row2.addWidget(self.input_file2)
    row2.addWidget(self.btn_browse2)

    file_layout.addLayout(row1)
    file_layout.addLayout(row2)
    main_layout.addWidget(file_panel)

    # --- Barre d'action : Comparer | Exporter | Effacer | Langue (EN par défaut) ---
    action_layout = QHBoxLayout()
    self.btn_compare = QPushButton()
    self.btn_compare.setObjectName("primaryButton")
    self.btn_compare.setFixedHeight(36)
    self.btn_compare.clicked.connect(self._start_comparison)

    self.btn_export = QPushButton()
    self.btn_export.setFixedHeight(36)
    self.btn_export.setEnabled(False)
    self.btn_export.clicked.connect(self._export_report)

    self.btn_clear = QPushButton()
    self.btn_clear.setFixedHeight(36)
    self.btn_clear.clicked.connect(self._clear_all)

    lang_icon = create_globe_icon("#4ec9b0")
    self.combo_lang = QComboBox()
    self.combo_lang.addItem(lang_icon, "EN", "EN")
    self.combo_lang.addItem(lang_icon, "FR", "FR")
    self.combo_lang.addItem(lang_icon, "AR", "AR")
    self.combo_lang.addItem(lang_icon, "RU", "RU")
    self.combo_lang.addItem(lang_icon, "ZH", "ZH")
    self.combo_lang.setFixedSize(78, 36)
    self.combo_lang.setToolTip("Language / Langue / اللغة / Язык / 语言")
    self.combo_lang.currentIndexChanged.connect(self._on_language_changed)

    action_layout.addWidget(self.btn_compare, stretch=3)
    action_layout.addWidget(self.btn_export, stretch=1)
    action_layout.addWidget(self.btn_clear, stretch=1)
    action_layout.addWidget(self.combo_lang)
    main_layout.addLayout(action_layout)

    # --- Barre de progression ---
    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setValue(0)
    self.progress_bar.hide()
    main_layout.addWidget(self.progress_bar)

    # --- Bandeau de statistiques ---
    stats_panel = QFrame()
    stats_panel.setObjectName("panel")
    stats_layout = QHBoxLayout(stats_panel)

    self.lbl_stat_size1 = QLabel()
    self.lbl_stat_size2 = QLabel()
    self.lbl_stat_diffs = QLabel()
    self.lbl_stat_blocks = QLabel()
    self.lbl_stat_sim = QLabel()

    for lbl in (
        self.lbl_stat_size1,
        self.lbl_stat_size2,
        self.lbl_stat_diffs,
        self.lbl_stat_blocks,
        self.lbl_stat_sim,
    ):
      lbl.setObjectName("statLabel")
      stats_layout.addWidget(lbl)

    main_layout.addWidget(stats_panel)

    # --- Inspecteur Hexadécimal Global Côte à Côte ---
    headers_layout = QHBoxLayout()
    self.h1 = QLabel()
    self.h1.setObjectName("hexHeader")
    self.h2 = QLabel()
    self.h2.setObjectName("hexHeader")
    headers_layout.addWidget(self.h1)
    headers_layout.addWidget(self.h2)
    main_layout.addLayout(headers_layout)

    hex_layout = QHBoxLayout()
    mono_font = QFont("Consolas", 10)
    mono_font.setStyleHint(QFont.StyleHint.Monospace)

    self.hex_view1 = QPlainTextEdit()
    self.hex_view1.setReadOnly(True)
    self.hex_view1.setFont(mono_font)
    self.hex_view1.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    self.hex_view1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    self.hex_view2 = QPlainTextEdit()
    self.hex_view2.setReadOnly(True)
    self.hex_view2.setFont(mono_font)
    self.hex_view2.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    self.hex_view2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    self.highlighter1 = HexDiffHighlighter(
        self.hex_view1.document(), is_modified_side=False
    )
    self.highlighter2 = HexDiffHighlighter(
        self.hex_view2.document(), is_modified_side=True
    )

    self.hex_view1.verticalScrollBar().valueChanged.connect(
        self.hex_view2.verticalScrollBar().setValue
    )
    self.hex_view2.verticalScrollBar().valueChanged.connect(
        self.hex_view1.verticalScrollBar().setValue
    )
    self.hex_view1.horizontalScrollBar().valueChanged.connect(
        self.hex_view2.horizontalScrollBar().setValue
    )
    self.hex_view2.horizontalScrollBar().valueChanged.connect(
        self.hex_view1.horizontalScrollBar().setValue
    )

    hex_layout.addWidget(self.hex_view1)
    hex_layout.addWidget(self.hex_view2)
    main_layout.addLayout(hex_layout, stretch=1)

  def _on_language_changed(self):
    self.current_lang = self.combo_lang.currentData()
    self._apply_language()

  def _apply_language(self):
    self.lbl1.setText(self._t("file1_label"))
    self.input_file1.setPlaceholderText(self._t("file1_placeholder"))
    self.lbl2.setText(self._t("file2_label"))
    self.input_file2.setPlaceholderText(self._t("file2_placeholder"))
    self.btn_browse1.setText(self._t("browse"))
    self.btn_browse2.setText(self._t("browse"))
    self.btn_compare.setText(self._t("compare"))
    self.btn_export.setText(self._t("export"))
    self.btn_clear.setText(self._t("clear"))
    self.h1.setText(self._t("hex_header1"))
    self.h2.setText(self._t("hex_header2"))

    if self.last_result is not None:
      self._display_results(self.last_result)
    else:
      self.lbl_stat_size1.setText(f"{self._t('stat_file1')} —")
      self.lbl_stat_size2.setText(f"{self._t('stat_file2')} —")
      self.lbl_stat_diffs.setText(f"{self._t('stat_diffs')} —")
      self.lbl_stat_blocks.setText(f"{self._t('stat_blocks')} —")
      self.lbl_stat_sim.setText(f"{self._t('stat_sim')} —")

  def _select_file(self, index: int):
    path, _ = QFileDialog.getOpenFileName(
        self,
        self._t("select_dialog").format(index=index),
        "",
        self._t("file_filter"),
    )
    if path:
      if index == 1:
        self.input_file1.setText(path)
      else:
        self.input_file2.setText(path)

  def _clear_all(self):
    self.render_timer.stop()
    self.last_result = None
    self.render_index = 0
    self.highlighter1.set_binaries(b"", b"")
    self.highlighter2.set_binaries(b"", b"")
    self.btn_export.setEnabled(False)
    self.input_file1.clear()
    self.input_file2.clear()
    self.hex_view1.clear()
    self.hex_view2.clear()
    self.progress_bar.hide()
    self._apply_language()

  def _start_comparison(self):
    path1 = self.input_file1.text().strip()
    path2 = self.input_file2.text().strip()

    if not path1 or not path2:
      QMessageBox.warning(
          self, self._t("warn_missing_title"), self._t("warn_missing_msg")
      )
      return

    if not os.path.isfile(path1) or not os.path.isfile(path2):
      QMessageBox.critical(
          self, self._t("err_title"), self._t("err_not_found")
      )
      return

    self.render_timer.stop()
    self.btn_compare.setEnabled(False)
    self.btn_export.setEnabled(False)
    self.hex_view1.clear()
    self.hex_view2.clear()
    self.progress_bar.setFormat(self._t("progress_scan"))
    self.progress_bar.setValue(0)
    self.progress_bar.show()

    self.worker = CompareWorker(path1, path2)
    self.worker.progress.connect(self.progress_bar.setValue)
    self.worker.finished.connect(self._on_comparison_finished)
    self.worker.error.connect(self._on_comparison_error)
    self.worker.start()

  def _on_comparison_error(self, message: str):
    self.progress_bar.hide()
    self.btn_compare.setEnabled(True)
    QMessageBox.critical(self, self._t("err_analysis_title"), message)

  def _on_comparison_finished(self, result: dict):
    self.btn_compare.setEnabled(True)
    self.btn_export.setEnabled(True)
    self.last_result = result
    self.highlighter1.set_binaries(result["data1"], result["data2"])
    self.highlighter2.set_binaries(result["data1"], result["data2"])
    self._display_results(result)

  def _display_results(self, result: dict):
    self.render_timer.stop()
    self.hex_view1.clear()
    self.hex_view2.clear()

    self.lbl_stat_size1.setText(
        f"{self._t('stat_file1')} {format_size(result['size1'])}"
    )
    self.lbl_stat_size2.setText(
        f"{self._t('stat_file2')} {format_size(result['size2'])}"
    )
    self.lbl_stat_diffs.setText(
        f"{self._t('stat_diffs')} {result['diff_bytes']:,}"
    )
    self.lbl_stat_blocks.setText(
        f"{self._t('stat_blocks')} {result['total_blocks']:,}"
    )
    self.lbl_stat_sim.setText(
        f"{self._t('stat_sim')} {result['similarity']:.2f}%"
    )

    total_blocks = result["total_blocks"]
    if total_blocks == 0:
      self.progress_bar.hide()
      self.hex_view1.setPlainText(self._t("identical_msg"))
      self.hex_view2.setPlainText(self._t("identical_msg"))
      return

    self.render_index = 0
    self.progress_bar.show()
    self._render_next_batch()
    if self.render_index < total_blocks:
      self.render_timer.start()

  def _render_next_batch(self):
    if self.last_result is None:
      self.render_timer.stop()
      return

    blocks = self.last_result["blocks"]
    total_blocks = len(blocks)
    data1 = self.last_result["data1"]
    data2 = self.last_result["data2"]

    start_idx = self.render_index
    end_idx = min(start_idx + self.BATCH_SIZE, total_blocks)

    lines1 = []
    lines2 = []
    header_tpl = self._t("block_header")

    for idx in range(start_idx, end_idx):
      start, end = blocks[idx]
      aligned_start = (start // 16) * 16
      aligned_end = ((end // 16) + 1) * 16

      header = header_tpl.format(
          idx=idx + 1, start=start, end=end, count=(end - start + 1)
      )
      lines1.append(header)
      lines2.append(header)

      for row_offset in range(aligned_start, aligned_end, 16):
        chunk1 = data1[row_offset : row_offset + 16]
        chunk2 = data2[row_offset : row_offset + 16]

        hex1_str = " ".join(f"{b:02X}" for b in chunk1)
        hex2_str = " ".join(f"{b:02X}" for b in chunk2)
        if len(chunk1) < 16:
          hex1_str += " --" * (16 - len(chunk1))
        if len(chunk2) < 16:
          hex2_str += " --" * (16 - len(chunk2))

        lines1.append(f"{row_offset:08X} | {hex1_str}")
        lines2.append(f"{row_offset:08X} | {hex2_str}")

      lines1.append("")
      lines2.append("")

    v_scroll = self.hex_view1.verticalScrollBar().value()
    self.hex_view1.appendPlainText("\n".join(lines1))
    self.hex_view2.appendPlainText("\n".join(lines2))
    self.hex_view1.verticalScrollBar().setValue(v_scroll)

    self.render_index = end_idx
    percent = int((self.render_index / total_blocks) * 100)
    self.progress_bar.setValue(percent)
    self.progress_bar.setFormat(
        self._t("progress_render").format(
            loaded=self.render_index, total=total_blocks
        )
    )

    if self.render_index >= total_blocks:
      self.render_timer.stop()
      self.progress_bar.hide()

  def _export_report(self):
    if self.last_result is None:
      return

    save_path, _ = QFileDialog.getSaveFileName(
        self,
        self._t("export_dialog"),
        "binary_comparison_report.txt",
        self._t("export_filter"),
    )
    if not save_path:
      return

    res = self.last_result
    blocks = res["blocks"]
    data1 = res["data1"]
    data2 = res["data2"]
    header_tpl = self._t("block_header")

    try:
      with open(save_path, "w", encoding="utf-8") as f:
        f.write("=========================================================\n")
        f.write(f"  {self._t('report_title')}\n")
        f.write("=========================================================\n")
        f.write(f"{self._t('stat_file1')} {res.get('path1', '')}\n")
        f.write(f"  Size : {format_size(res['size1'])}\n")
        f.write(f"{self._t('stat_file2')} {res.get('path2', '')}\n")
        f.write(f"  Size : {format_size(res['size2'])}\n")
        f.write("---------------------------------------------------------\n")
        f.write(f"{self._t('stat_diffs')} {res['diff_bytes']:,}\n")
        f.write(f"{self._t('stat_blocks')} {res['total_blocks']:,}\n")
        f.write(f"{self._t('stat_sim')} {res['similarity']:.2f}%\n")
        f.write("=========================================================\n\n")

        if not blocks:
          f.write(self._t("identical_msg") + "\n")
        else:
          for idx, (start, end) in enumerate(blocks, start=1):
            aligned_start = (start // 16) * 16
            aligned_end = ((end // 16) + 1) * 16

            f.write(
                header_tpl.format(
                    idx=idx, start=start, end=end, count=(end - start + 1)
                )
                + "\n"
            )
            f.write(
                f"  [{self._t('report_orig')}]                          || "
                f"[{self._t('report_mod')}]\n"
            )

            for row_offset in range(aligned_start, aligned_end, 16):
              chunk1 = data1[row_offset : row_offset + 16]
              chunk2 = data2[row_offset : row_offset + 16]

              hex1_str = " ".join(f"{b:02X}" for b in chunk1)
              hex2_str = " ".join(f"{b:02X}" for b in chunk2)
              if len(chunk1) < 16:
                hex1_str += " --" * (16 - len(chunk1))
              if len(chunk2) < 16:
                hex2_str += " --" * (16 - len(chunk2))

              f.write(
                  f"{row_offset:08X} | {hex1_str}  ||  {hex2_str}\n"
              )
            f.write("\n")

      QMessageBox.information(
          self,
          self._t("export_success_title"),
          self._t("export_success_msg").format(
              total=len(blocks), path=save_path
          ),
      )
    except Exception as exc:
      QMessageBox.critical(self, self._t("export_err_title"), str(exc))


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = BinaryComparatorWindow()
  window.show()
  sys.exit(app.exec())