import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import { DashboardData, NavView } from './types';
import { uploadStatement, loadDemoStatement, purgeSession } from './api';
import { Navbar } from './components/Navbar';
import { LandingPage } from './components/LandingPage';
import { UploadModal } from './components/UploadModal';
import { ProcessingModal } from './components/ProcessingModal';
import { OverviewDashboard } from './components/OverviewDashboard';
import { TransactionsView } from './components/TransactionsView';
import { SpendingView } from './components/SpendingView';
import { SubscriptionsView } from './components/SubscriptionsView';
import { AnomaliesView } from './components/AnomaliesView';
import { TaxHelperView } from './components/TaxHelperView';
import { SettingsView } from './components/SettingsView';
import { AIAssistantModal } from './components/AIAssistantModal';
import { SAMPLE_STATEMENT_A, SAMPLE_STATEMENT_B, SAMPLE_STATEMENT_C } from './sampleStatements';

export function App() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [currentView, setCurrentView] = useState<NavView>('overview');
  const [isUploadOpen, setIsUploadOpen] = useState<boolean>(false);
  const [isProcessingOpen, setIsProcessingOpen] = useState<boolean>(false);
  const [isAssistantOpen, setIsAssistantOpen] = useState<boolean>(false);
  const [processingFilename, setProcessingFilename] = useState<string>('bank_statement.csv');
  const [pendingResult, setPendingResult] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Trigger confetti if high financial health
  const triggerCelebration = (score: number) => {
    if (score >= 70) {
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.6 },
        colors: ['#10B981', '#38BDF8', '#8B5CF6'],
      });
    }
  };

  // Upload Statement handler
  const handleFileSelected = async (file: File) => {
    setUploadError(null);
    setProcessingFilename(file.name);
    setIsUploadOpen(false);
    setIsProcessingOpen(true);
    setIsLoading(true);

    try {
      const data = await uploadStatement(file);
      setPendingResult(data);
    } catch (err: any) {
      console.error(err);
      setIsProcessingOpen(false);
      setIsLoading(false);
      setUploadError(err.message || 'We could not process this statement. Please check the file.');
      setIsUploadOpen(true);
    }
  };

  // Demo Statement handler
  const handleTryDemo = async () => {
    setUploadError(null);
    setProcessingFilename('HDFC_Bank_Demo_Statement.csv');
    setIsUploadOpen(false);
    setIsProcessingOpen(true);
    setIsLoading(true);

    try {
      const data = await loadDemoStatement();
      setPendingResult(data);
    } catch (err: any) {
      console.error(err);
      setIsProcessingOpen(false);
      setIsLoading(false);
      alert('Failed to load demo statement.');
    }
  };

  // Sample Statements A, B, C instant runner
  const handleLoadSample = (sampleKey: 'a' | 'b' | 'c') => {
    let content = '';
    let name = '';

    if (sampleKey === 'a') {
      content = SAMPLE_STATEMENT_A;
      name = 'statement_a_corporate_salary.csv';
    } else if (sampleKey === 'b') {
      content = SAMPLE_STATEMENT_B;
      name = 'statement_b_freelancer_irregular.csv';
    } else {
      content = SAMPLE_STATEMENT_C;
      name = 'statement_c_minimalist_no_subscriptions.csv';
    }

    const file = new File([content], name, { type: 'text/csv' });
    handleFileSelected(file);
  };

  // When sequential processing animation completes
  const handleProcessingComplete = () => {
    if (pendingResult) {
      setDashboardData(pendingResult);
      setPendingResult(null);
      setCurrentView('overview');
      triggerCelebration(pendingResult.health_score);
    }
    setIsProcessingOpen(false);
    setIsLoading(false);
  };

  // Purge Session handler (Privacy)
  const handlePurgeSession = async () => {
    if (dashboardData?.session_id) {
      await purgeSession(dashboardData.session_id);
    }
    setDashboardData(null);
    setCurrentView('overview');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500/30 selection:text-emerald-300">
      {/* Navigation Bar */}
      <Navbar
        currentView={currentView}
        onViewChange={(view) => {
          if (view === 'assistant') {
            setIsAssistantOpen(true);
          } else {
            setCurrentView(view);
          }
        }}
        onOpenUpload={() => setIsUploadOpen(true)}
        onOpenAssistant={() => setIsAssistantOpen(true)}
        onDeleteSession={handlePurgeSession}
        isDemo={dashboardData?.is_demo ?? false}
        hasSession={!!dashboardData}
        filename={dashboardData?.filename}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {!dashboardData ? (
          <LandingPage
            onOpenUpload={() => setIsUploadOpen(true)}
            onLoadDemo={handleTryDemo}
            onLoadSample={handleLoadSample}
            isLoading={isLoading}
          />
        ) : (
          <div>
            {currentView === 'overview' && (
              <OverviewDashboard
                data={dashboardData}
                onNavigate={(v) => setCurrentView(v)}
                onOpenAssistant={() => setIsAssistantOpen(true)}
              />
            )}

            {currentView === 'transactions' && (
              <TransactionsView sessionId={dashboardData.session_id} />
            )}

            {currentView === 'spending' && (
              <SpendingView
                categories={dashboardData.category_breakdown}
                totalExpenses={dashboardData.total_expenses}
              />
            )}

            {currentView === 'subscriptions' && (
              <SubscriptionsView
                subscriptions={dashboardData.subscriptions}
                recurringMonthlySpend={dashboardData.recurring_monthly_spend}
              />
            )}

            {currentView === 'anomalies' && (
              <AnomaliesView anomalies={dashboardData.anomalies} />
            )}

            {currentView === 'tax' && (
              <TaxHelperView taxSummary={dashboardData.tax_summary} />
            )}

            {currentView === 'settings' && (
              <SettingsView
                data={dashboardData}
                onPurgeData={handlePurgeSession}
              />
            )}
          </div>
        )}
      </main>

      {/* Upload Modal */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onFileSelected={handleFileSelected}
        onTryDemo={handleTryDemo}
        onSelectSample={handleLoadSample}
      />

      {/* Processing Animation Modal */}
      <ProcessingModal
        isOpen={isProcessingOpen}
        filename={processingFilename}
        onComplete={handleProcessingComplete}
      />

      {/* AI Assistant Chat Modal */}
      {dashboardData && (
        <AIAssistantModal
          isOpen={isAssistantOpen}
          onClose={() => setIsAssistantOpen(false)}
          sessionId={dashboardData.session_id}
        />
      )}
    </div>
  );
}

export default App;
