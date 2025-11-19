import { useState } from 'react';
import toast from 'react-hot-toast';

const MobileMoneyPrompt = ({ order, phone, amount, onComplete, onCancel }) => {
  const [pin, setPin] = useState('');
  const [processing, setProcessing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (pin.length < 4) {
      toast.error('Please enter your mobile money PIN');
      return;
    }

    setProcessing(true);
    
    // Simulate payment processing (in production, this would verify with payment gateway)
    // For now, we'll just mark it as completed after a short delay
    setTimeout(() => {
      toast.success('Mobile money payment successful!');
      onComplete();
      setProcessing(false);
    }, 2000);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold mb-4">Mobile Money Payment</h2>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <p className="text-sm text-gray-600 mb-2 font-semibold">📱 You will receive a USSD prompt on your phone ({phone}):</p>
          <div className="bg-white rounded p-3 font-mono text-sm border border-blue-300">
            <div className="mb-2 flex justify-between">
              <span className="text-gray-600">To:</span>
              <span className="font-semibold">ChickOrder</span>
            </div>
            <div className="mb-2 flex justify-between">
              <span className="text-gray-600">Amount:</span>
              <span className="font-semibold text-primary-600">GHS {amount.toFixed(2)}</span>
            </div>
            <div className="mb-2 flex justify-between">
              <span className="text-gray-600">Phone:</span>
              <span className="font-semibold">{phone}</span>
            </div>
            <div className="mb-2 flex justify-between">
              <span className="text-gray-600">Reference:</span>
              <span className="font-semibold">{order.order_number}</span>
            </div>
          </div>
          <p className="text-xs text-blue-700 mt-2">
            ⚠️ Check your phone now for the USSD prompt. Enter your mobile money PIN to authorize the payment.
          </p>
        </div>

        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">
            Check your phone ({phone}) for the USSD prompt. Enter your mobile money PIN when prompted.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Enter Mobile Money PIN (for testing)</label>
            <input
              type="password"
              className="input"
              placeholder="Enter 4-digit PIN"
              value={pin}
              onChange={(e) => setPin(e.target.value.replace(/\D/g, '').slice(0, 4))}
              maxLength={4}
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              In production, this would be entered on your phone via USSD
            </p>
          </div>

          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onCancel}
              className="btn btn-secondary flex-1"
              disabled={processing}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary flex-1"
              disabled={processing || pin.length < 4}
            >
              {processing ? 'Processing...' : 'Confirm Payment'}
            </button>
          </div>
        </form>

        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <p className="text-xs text-yellow-800">
            <strong>Note:</strong> This is a simulation. In production, you would receive an actual USSD prompt on your phone to authorize the payment.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MobileMoneyPrompt;

