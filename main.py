import sys
print("Python path:", sys.executable)
print("Python version:", sys.version)

import os
print("Current directory:", os.getcwd())
print("sys.path:", sys.path)

input("Нажмите Enter для продолжения...")
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forms.login_form import LoginForm

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()