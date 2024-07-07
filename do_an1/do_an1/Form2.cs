using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace do_an1
{
    public partial class Form2 : Form
    {
       
        public Form2()
        {
            InitializeComponent();
           
        }
        private void addUserControl(UserControl userControl)
        {
            userControl.Dock = DockStyle.Fill;
            Panel3.Controls.Clear();
            Panel3.Controls.Add(userControl);
            userControl.BringToFront();


        }

        private void btbKQ_Click(object sender, EventArgs e)
        {
            UserControl1 userControl = new UserControl1();
            addUserControl(userControl);
            HighlightButton((Guna.UI2.WinForms.Guna2Button)sender);
        }

        private void btnDC_Click(object sender, EventArgs e)
        {
            UserControl2 userControl = new UserControl2();
            addUserControl(userControl);
            HighlightButton((Guna.UI2.WinForms.Guna2Button)sender);
        }

        private void btnDS_Click(object sender, EventArgs e)
        {
            UserControl3 userControl = new UserControl3();
            addUserControl(userControl);
            HighlightButton((Guna.UI2.WinForms.Guna2Button)sender);
        }
        private Guna.UI2.WinForms.Guna2Button currentButton;

        private void HighlightButton(Guna.UI2.WinForms.Guna2Button btn)
        {
            if (currentButton != null)
            {
                ResetButtonColor();
            }

            // Lưu Guna2Button hiện tại
            currentButton = btn;

            // Đặt màu nền mới cho Guna2Button hiện tại
            currentButton.FillColor = Color.FromArgb(34, 34, 34);
            currentButton.CustomBorderColor = Color.FromArgb(190, 0, 0);
            currentButton.ForeColor = Color.FromArgb(190, 0, 0);

            // Thực hiện các hành động khác nếu cần
            // ...
        }

        private void ResetButtonColor()
        {
            if (currentButton != null)
            {
                // Reset màu nền của Guna2Button về màu mặc định
                currentButton.FillColor = Color.FromArgb(34, 34, 34);
                currentButton.CustomBorderColor = Color.FromArgb(34, 34, 34);
                currentButton.ForeColor = Color.White;
            }
        }
    }
}
