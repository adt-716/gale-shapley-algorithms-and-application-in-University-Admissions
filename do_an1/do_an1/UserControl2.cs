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
    public partial class UserControl2 : UserControl
    {
       
        public UserControl2()
        {
            InitializeComponent();
        }

        private void btnTraCuu2_Click(object sender, EventArgs e)
        {
            string maNganh = txtMaNganh.Text;

            // Mở file Excel
            Excel.Application excelApp = new Excel.Application();
            Excel.Workbook workbook = excelApp.Workbooks.Open("D:\\Do an\\chi_tieu.xlsx");
            Excel.Worksheet worksheet = workbook.Sheets[1];
            Excel.Range range = worksheet.UsedRange;

            // Tìm kiếm thông tin trong file Excel
            bool found = false;
            for (int i = 2; i <= range.Rows.Count; i++)
            {
                string maNganhFromExcel = Convert.ToString((range.Cells[i, 1] as Excel.Range).Value2);
                if (maNganhFromExcel == maNganh)
                {
                    found = true;
                    string tenNganh = Convert.ToString((range.Cells[i, 2] as Excel.Range).Value2);
                    string maNganhChuan = Convert.ToString((range.Cells[i, 3] as Excel.Range).Value2);
                    int chiTieu = Convert.ToInt32((range.Cells[i, 4] as Excel.Range).Value2);
                    double diemChuan = Convert.ToDouble((range.Cells[i, 5] as Excel.Range).Value2);

                    // Hiển thị thông tin lên giao diện
                    txtTenNganh.Text = tenNganh;
                    txtMaNganhChuan.Text = maNganhChuan;
                    txtChiTieu.Text = chiTieu.ToString();
                    txtDiemChuan.Text = diemChuan.ToString();

                    break;
                }
            }

            // Đóng file Excel
            workbook.Close(false);
            excelApp.Quit();

            // Kiểm tra nếu không tìm thấy
            if (!found)
            {
                MessageBox.Show("Không tìm thấy thông tin cho mã ngành này.", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            Excel.Application excelAppNew = new Excel.Application();
            Excel.Workbook workbookNew = excelAppNew.Workbooks.Open("D:\\Do an\\ket_qua.xlsx");
            Excel.Worksheet worksheetNew = workbookNew.Sheets[1];
            Excel.Range rangeNew = worksheetNew.UsedRange;
            System.Data.DataTable dataTable = new System.Data.DataTable();
            dataTable.Columns.Add("CCCD");
            dataTable.Columns.Add("Tên");
            dataTable.Columns.Add("Thứ tự nguyện vọng");
            dataTable.Columns.Add("Điểm xét");
            for (int i = 2; i <= rangeNew.Rows.Count; i++)
            {
                string maNganhFromExcelNew = Convert.ToString((rangeNew.Cells[i, 3] as Excel.Range).Value2);
                if (maNganhFromExcelNew == maNganh)
                {
                    DataRow row = dataTable.NewRow();
                    row["CCCD"] = Convert.ToString((rangeNew.Cells[i, 1] as Excel.Range).Value2);
                    row["Tên"] = Convert.ToString((rangeNew.Cells[i, 2] as Excel.Range).Value2);
                    row["Thứ tự nguyện vọng"] = Convert.ToString((rangeNew.Cells[i, 4] as Excel.Range).Value2);
                    row["Điểm xét"] = Convert.ToString((rangeNew.Cells[i, 5] as Excel.Range).Value2);
                    dataTable.Rows.Add(row);
                }
            }

            // Đóng file Excel mới
            workbookNew.Close(false);
            excelAppNew.Quit();

            // Hiển thị dữ liệu trong DataGridView
            DataGridView2.DataSource = dataTable;
        }

        private void btnHuy2_Click(object sender, EventArgs e)
        {
            txtMaNganh.Text = "";
        }
    }
    
}

