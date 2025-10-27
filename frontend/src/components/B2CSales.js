import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

// Get API URL from environment variable (for production) or use localhost (for development)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Debug: Log the API URL being used
console.log('Using API URL:', API_BASE_URL);

function B2CSales() {
  const [portal, setPortal] = useState('amazon');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [csvFilename, setCsvFilename] = useState(null);
  const [b2bFilename, setB2bFilename] = useState(null);
  const [previewData, setPreviewData] = useState([]);
  const [b2csRowCount, setB2csRowCount] = useState(0);
  const [b2bRowCount, setB2bRowCount] = useState(0);
  const [b2csTaxableValue, setB2csTaxableValue] = useState(0);
  const [b2bTaxableValue, setB2bTaxableValue] = useState(0);

  const onDrop = async (acceptedFiles) => {
    setError(null);
    setSuccess(null);

    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('portal', portal);

      console.log('Uploading to:', `${API_BASE_URL}/upload`);

      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        const reportFreq = response.data.report_frequency || 'monthly';
        setSuccess(`File uploaded successfully! ${response.data.rows_processed} rows processed. (${reportFreq} report)`);
        setUploadedFiles([...uploadedFiles, {
          filename: response.data.filename,
          portal,
          originalName: file.name,
          rows: response.data.rows_processed,
          reportFrequency: reportFreq,
          gstin: response.data.gstin, // Store GSTIN
        }]);
        setPreviewData(response.data.data);
        
        // Show debug info if available
        if (response.data.debug_info && response.data.debug_info.length > 0) {
          console.log('Debug Info:', response.data.debug_info);
          alert('Debug Info:\n' + response.data.debug_info.join('\n'));
        }
      }
    } catch (err) {
      console.error('Upload error:', err);
      console.error('Error response:', err.response);
      console.error('Error message:', err.message);
      const errorMessage = err.response?.data?.error || err.message || 'Failed to upload file';
      console.error('Setting error:', errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv'],
    },
    multiple: false,
  });

  const handleGenerateCSV = async () => {
    if (uploadedFiles.length === 0) {
      setError('Please upload at least one file');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Get report frequency from uploaded file
      const reportFreq = uploadedFiles[0]?.reportFrequency || 'monthly';
      const gstin = uploadedFiles[0]?.gstin || null;
      
      const response = await axios.post(`${API_BASE_URL}/generate-csv`, {
        data: previewData, // In production, this would be the full merged data
        report_frequency: reportFreq,
        gstin: gstin, // Include GSTIN in request
      });

      if (response.data.success) {
        setSuccess(`B2CS CSV generated successfully! ${response.data.rows} rows.`);
        setCsvFilename(response.data.filename);
        setB2csRowCount(response.data.rows || 0);
        setB2csTaxableValue(response.data.total_taxable_value || 0);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate CSV');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateB2B = async () => {
    if (uploadedFiles.length === 0) {
      setError('Please upload at least one file');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Get report frequency from uploaded file
      const reportFreq = uploadedFiles[0]?.reportFrequency || 'monthly';
      const gstin = uploadedFiles[0]?.gstin || null;
      
      const response = await axios.post(`${API_BASE_URL}/generate-b2b`, {
        filename: uploadedFiles[0].filename,
        report_frequency: reportFreq,
        gstin: gstin, // Include GSTIN in request
      });

      if (response.data.success) {
        setSuccess(`B2B CSV generated successfully! ${response.data.rows} rows.`);
        setB2bFilename(response.data.filename);
        setB2bRowCount(response.data.rows || 0);
        setB2bTaxableValue(response.data.total_taxable_value || 0);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate B2B CSV');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCSV = async () => {
    if (csvFilename) {
      try {
        const response = await axios.get(`${API_BASE_URL}/download/${csvFilename}`, {
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', csvFilename);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        setError('Failed to download B2CS CSV');
      }
    }
  };

  const handleDownloadB2B = async () => {
    if (b2bFilename) {
      try {
        const response = await axios.get(`${API_BASE_URL}/download/${b2bFilename}`, {
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', b2bFilename);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        setError('Failed to download B2B CSV');
      }
    }
  };

  const handleDownloadAll = async () => {
    if (csvFilename && b2bFilename) {
      // Download both files - first B2CS, then B2B
      await handleDownloadCSV();
      // Small delay to ensure first download completes
      await new Promise(resolve => setTimeout(resolve, 300));
      await handleDownloadB2B();
    } else if (csvFilename) {
      await handleDownloadCSV();
    } else if (b2bFilename) {
      await handleDownloadB2B();
    }
  };

  const handleRemoveFile = (filename) => {
    setUploadedFiles(uploadedFiles.filter(f => f.filename !== filename));
    if (uploadedFiles.length === 1) {
      setPreviewData([]);
      // Clear generated CSV states
      setCsvFilename(null);
      setB2bFilename(null);
      setB2csRowCount(0);
      setB2bRowCount(0);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        GSTR-1 CSV Generator
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Upload Amazon "Ready to File" reports to generate B2CS (B2C Small) and B2B CSV files for GST returns
      </Typography>

      <Card sx={{ mt: 3, mb: 3 }}>
        <CardContent>
          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Currently Supported: Amazon Seller Central - "Ready to File" Report
            </Typography>
            <Typography variant="body2">
              Download your quarterly GST report from Amazon Seller Central → Reports → Tax Documents → GST Returns → Ready to File
            </Typography>
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              ✅ Generate B2CS (B2C Small) CSV for aggregated B2C sales
              <br />
              ✅ Generate B2B CSV for all B2B invoices
              <br />
              💡 Additional portals (Flipkart, Pepperfry, etc.) coming soon!
            </Typography>
          </Alert>

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Select Portal</InputLabel>
            <Select
              value={portal}
              label="Select Portal"
              onChange={(e) => setPortal(e.target.value)}
              disabled={false} // Keep enabled for now, will filter on backend
            >
              <MenuItem value="amazon">Amazon - Ready to File Report</MenuItem>
              <MenuItem value="flipkart" disabled>Flipkart (Coming Soon)</MenuItem>
              <MenuItem value="pepperfry" disabled>Pepperfry (Coming Soon)</MenuItem>
              <MenuItem value="custom" disabled>Custom/Other Portal (Coming Soon)</MenuItem>
            </Select>
          </FormControl>

          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              bgcolor: isDragActive ? 'action.hover' : 'background.paper',
              transition: 'all 0.2s',
            }}
          >
            <input {...getInputProps()} />
            <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Drop the file here' : 'Drag & drop your file here'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              or click to browse
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
              Supports: .xlsx, .xls, .csv
            </Typography>
          </Box>

          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}
        </CardContent>
      </Card>

      {uploadedFiles.length > 0 && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Uploaded Files
            </Typography>
            {uploadedFiles.map((file, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  p: 2,
                  bgcolor: 'background.default',
                  borderRadius: 1,
                  mb: 1,
                }}
              >
                <Box>
                  <Typography variant="body1">{file.originalName}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Portal: {file.portal} | {file.reportFrequency || 'monthly'} report | Rows: {file.rows}
                  </Typography>
                </Box>
                <Button
                  color="error"
                  size="small"
                  startIcon={<DeleteIcon />}
                  onClick={() => handleRemoveFile(file.filename)}
                >
                  Remove
                </Button>
              </Box>
            ))}
          </CardContent>
        </Card>
      )}

      {(b2csRowCount > 0 || b2bRowCount > 0) && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Generated CSV Summary
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 3, mt: 2 }}>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  B2CS Records
                </Typography>
                <Typography variant="h5" color="primary.main" fontWeight="bold">
                  {b2csRowCount}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  ₹ {b2csTaxableValue.toLocaleString('en-IN', {maximumFractionDigits: 2})}
                </Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  B2B Records
                </Typography>
                <Typography variant="h5" color="secondary.main" fontWeight="bold">
                  {b2bRowCount}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  ₹ {b2bTaxableValue.toLocaleString('en-IN', {maximumFractionDigits: 2})}
                </Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Total Taxable Value
                </Typography>
                <Typography variant="h5" color="success.main" fontWeight="bold">
                  ₹ {(b2csTaxableValue + b2bTaxableValue).toLocaleString('en-IN', {maximumFractionDigits: 2})}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      )}

      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          size="large"
          onClick={handleGenerateCSV}
          disabled={uploadedFiles.length === 0 || loading}
          color="primary"
        >
          Generate B2CS CSV
        </Button>
        <Button
          variant="contained"
          size="large"
          onClick={handleGenerateB2B}
          disabled={uploadedFiles.length === 0 || loading}
          color="secondary"
        >
          Generate B2B CSV
        </Button>
        {(csvFilename || b2bFilename) && (
          <Button
            variant="contained"
            size="large"
            startIcon={<DownloadIcon />}
            onClick={handleDownloadAll}
            color="success"
          >
            {csvFilename && b2bFilename ? 'Download All CSVs' : csvFilename ? 'Download B2CS' : 'Download B2B'}
          </Button>
        )}
      </Box>
    </Box>
  );
}

export default B2CSales;
