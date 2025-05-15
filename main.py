import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from views.main_window import MainWindow
from controllers.calculator_controller import CalculatorController


def main():
    """应用程序入口"""
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        # 初始化MVC
        view = MainWindow()
        controller = CalculatorController(view)

        view.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application crashed: {str(e)}")
        import traceback
        traceback.print_exc()
        # 显示错误对话框
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText("应用程序发生严重错误")
        error_box.setInformativeText(str(e))
        error_box.setWindowTitle("错误")
        error_box.exec_()


if __name__ == "__main__":
    main()