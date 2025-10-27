import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
} from '@mui/material';
import {
  Description as DescriptionIcon,
  Assignment as AssignmentIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

const featureCards = [
  {
    title: 'GSTR-1 B2C Sales',
    description: 'Generate B2C sales CSV from multiple portals',
    icon: <DescriptionIcon sx={{ fontSize: 40 }} color="primary" />,
    path: '/gstr1/b2c-sales',
    color: '#1976d2',
  },
  {
    title: 'GSTR-3B',
    description: 'Coming soon - GSTR-3B return filing',
    icon: <AssignmentIcon sx={{ fontSize: 40 }} color="secondary" />,
    path: '/gstr3b',
    color: '#dc004e',
    comingSoon: true,
  },
  {
    title: 'Analytics',
    description: 'View sales analytics and reports',
    icon: <TrendingUpIcon sx={{ fontSize: 40 }} color="success" />,
    path: '/analytics',
    color: '#2e7d32',
    comingSoon: true,
  },
];

function Dashboard() {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Welcome to SellerSuite
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Your complete business management platform for Indian sellers. Starting with GST returns - more features coming soon.
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {featureCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center', py: 4 }}>
                {card.icon}
                <Typography variant="h5" component="h2" gutterBottom mt={2}>
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.description}
                </Typography>
                {card.comingSoon && (
                  <Typography
                    variant="caption"
                    color="warning.main"
                    sx={{ display: 'block', mt: 1 }}
                  >
                    Coming Soon
                  </Typography>
                )}
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button
                  size="small"
                  variant="contained"
                  onClick={() => navigate(card.path)}
                  disabled={card.comingSoon}
                >
                  {card.comingSoon ? 'Coming Soon' : 'Get Started'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4, p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          How it Works
        </Typography>
        <Typography variant="body2" color="text.secondary">
          1. Upload sales data from your selling portals (Amazon, Flipkart, etc.)<br />
          2. Review and merge data from multiple sources<br />
          3. Generate GST-compliant CSV files<br />
          4. Upload to GST portal and file your returns
        </Typography>
      </Box>
    </Box>
  );
}

export default Dashboard;
