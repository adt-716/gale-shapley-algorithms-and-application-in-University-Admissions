using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using OfficeOpenXml;
using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Office.Interop.Excel;
 
namespace do_an1
{
    public partial class Form1 : Form
    {
        private System.Data.DataTable dataTable;
        private string verificationCode;
        private object label5;

        public Form1()
        {
            InitializeComponent();
            GenerateVerificationCode();
            DisplayExcelData("D:\\Do an\\ket_qua.xlsx");
            
        }
        private void DisplayExcelData(string excelFilePath, string filter = "")
        {
            Excel.Application excelApp = new Excel.Application();
            Workbook excelWorkbook = null;
            Worksheet excelWorksheet = null;
            Range excelRange = null;

            try
            {
                excelWorkbook = excelApp.Workbooks.Open(excelFilePath);
                excelWorksheet = excelWorkbook.Sheets[1];
                excelRange = excelWorksheet.UsedRange;

                int rowCount = excelRange.Rows.Count;
                int colCount = excelRange.Columns.Count;

                dataTable = new System.Data.DataTable();

                for (int col = 1; col <= colCount; col++)
                {
                    string columnName = (excelRange.Cells[1, col] as Range).Value2?.ToString() ?? $"Column{col}";
                    dataTable.Columns.Add(columnName, typeof(string));
                }

                object[,] valueArray = (object[,])excelRange.Value2;

                for (int row = 2; row <= rowCount; row++)
                {
                    DataRow dr = dataTable.NewRow();
                    for (int col = 1; col <= colCount; col++)
                    {
                        dr[col - 1] = valueArray[row, col]?.ToString() ?? string.Empty;
                    }
                    dataTable.Rows.Add(dr);
                }

                DataView dv = new DataView(dataTable);
                dv.RowFilter = !string.IsNullOrEmpty(filter) ? $"[CCCD] LIKE '%{filter}%'" : string.Empty;
                DataGridView1.DataSource = dv;

                if (dv.Count == 0)
                {
                    MessageBox.Show("Bạn không đỗ", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }
            finally
            {
                if (excelWorkbook != null) excelWorkbook.Close(false);
                if (excelApp != null) excelApp.Quit();

                ReleaseObject(excelRange);
                ReleaseObject(excelWorksheet);
                ReleaseObject(excelWorkbook);
                ReleaseObject(excelApp);
            }
        }
        
        private void ReleaseObject(object obj)
        {
            try
            {
                if (obj != null)
                {
                    System.Runtime.InteropServices.Marshal.ReleaseComObject(obj);
                    obj = null;
                }
            }
            catch (Exception ex)
            {
                obj = null;
                MessageBox.Show("Exception occurred while releasing object " + ex.ToString());
            }
            finally
            {
                GC.Collect();
            }
        }

        private void btnTraCuu_Click(object sender, EventArgs e)
        {
            string filter = txt_CCCD.Text;
            string userCode = txtMa.Text;

            if (userCode != verificationCode)
            {
                MessageBox.Show("Mã xác nhận không đúng", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                GenerateVerificationCode();
                return;
            }

            DisplayExcelData("D:\\Do an\\ket_qua.xlsx", filter);
            GenerateVerificationCode(); // Tạo mã xác nhận mới

        }
        
        private void GenerateVerificationCode()
        {
            Random random = new Random();
            verificationCode = random.Next(1000, 9999).ToString();
            lbMa.Text = verificationCode;
        }

        private void btnTraCuu2_Click(object sender, EventArgs e)
        {
            string maNganh = txtMaNganh.Text;
            if (string.IsNullOrEmpty(maNganh))
            {
                MessageBox.Show("Vui lòng nhập mã ngành", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            Excel.Application excelApp = new Excel.Application();
            Workbook excelWorkbook = null;
            Worksheet excelWorksheet = null;
            Range excelRange = null;

            try
            {
                excelWorkbook = excelApp.Workbooks.Open("D:\\Do an\\diem_chuan.xlsx"); // Đường dẫn tới file điểm chuẩn
                excelWorksheet = excelWorkbook.Sheets[1];
                excelRange = excelWorksheet.UsedRange;

                int rowCount = excelRange.Rows.Count;
                int colCount = excelRange.Columns.Count;

                System.Data.DataTable diemChuanTable = new System.Data.DataTable();

                for (int col = 1; col <= colCount; col++)
                {
                    string columnName = (excelRange.Cells[1, col] as Range).Value2?.ToString() ?? $"Column{col}";
                    diemChuanTable.Columns.Add(columnName, typeof(string));
                }

                object[,] valueArray = (object[,])excelRange.Value2;

                for (int row = 2; row <= rowCount; row++)
                {
                    DataRow dr = diemChuanTable.NewRow();
                    for (int col = 1; col <= colCount; col++)
                    {
                        dr[col - 1] = valueArray[row, col]?.ToString() ?? string.Empty;
                    }
                    diemChuanTable.Rows.Add(dr);
                }

                DataView dv = new DataView(diemChuanTable);
                dv.RowFilter = $"[MaNganh] = '{maNganh}'";

                if (dv.Count == 0)
                {
                    MessageBox.Show("Không tìm thấy mã ngành", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                // Hiển thị thông tin điểm chuẩn lên các TextBox
                txtTenNganh.Text = dv[0]["TenNganh"].ToString();
                txtDiemChuan.Text = dv[0]["DiemChuan"].ToString();

                // Hiển thị danh sách sinh viên đỗ ngành đó vào DataGridView
                dv.RowFilter = $"[MaNganh] = '{maNganh}' AND [Diem] >= {txtDiemChuan.Text}";
                DataGridView2.DataSource = dv;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }
            finally
            {
                if (excelWorkbook != null) excelWorkbook.Close(false);
                if (excelApp != null) excelApp.Quit();

                ReleaseObject(excelRange);
                ReleaseObject(excelWorksheet);
                ReleaseObject(excelWorkbook);
                ReleaseObject(excelApp);
            }
        }
    }
    
}
