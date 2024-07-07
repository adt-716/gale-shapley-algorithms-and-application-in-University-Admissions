using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Office.Interop.Excel;

namespace do_an1
{
    public partial class UserControl3 : UserControl
    {
        public UserControl3()
        {
            InitializeComponent();
        }

        private void UserControl3_Load(object sender, EventArgs e)
        {
            // Tạo một ứng dụng Excel mới
            Excel.Application excelApp = new Excel.Application();

            // Mở workbook
            Excel.Workbook workbook = excelApp.Workbooks.Open("D:\\Do an\\chi_tieu.xlsx");

            // Lấy sheet đầu tiên từ workbook
            Excel.Worksheet worksheet = workbook.Sheets[1];

            // Lấy phạm vi dữ liệu sử dụng
            Excel.Range range = worksheet.UsedRange;

            // Tạo DataTable để lưu dữ liệu từ Excel
            System.Data.DataTable dataTable = new System.Data.DataTable();

            // Lặp qua từng hàng trong phạm vi dữ liệu và thêm vào DataTable
            for (int row = 1; row <= range.Rows.Count; row++)
            {
                DataRow newRow = dataTable.NewRow();
                for (int col = 1; col <= range.Columns.Count; col++)
                {
                    if (row == 1) // Nếu là hàng đầu tiên, thêm cột mới cho DataTable
                    {
                        dataTable.Columns.Add((range.Cells[row, col] as Excel.Range).Value2.ToString());
                    }
                    else // Nếu không, thêm dữ liệu từ cell vào DataRow
                    {
                        newRow[col - 1] = (range.Cells[row, col] as Excel.Range).Value2;
                    }
                }
                // Thêm DataRow vào DataTable
                dataTable.Rows.Add(newRow);
            }

            // Đóng workbook và ứng dụng Excel
            workbook.Close(false);
            excelApp.Quit();

            // Gán DataTable làm nguồn dữ liệu cho DataGridView
            DataGridView3.DataSource = dataTable;
        }
    }
}
