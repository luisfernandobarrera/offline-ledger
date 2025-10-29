# Double-Entry Accounting App

A feature-complete, offline-first double-entry accounting application built with Reflex. This application follows Material Design 3 principles with an emerald theme and JetBrains Mono font.

## 🚀 Features

### Core Accounting
- **Double-Entry Accounting System**: Full implementation of double-entry bookkeeping principles
- **Chart of Accounts**: Manage accounts across 5 categories (Assets, Liabilities, Equity, Revenue, Expenses)
- **Transaction Management**: Create, view, and filter transactions with automatic balance validation
- **Account Balances**: Real-time balance calculations with proper debit/credit handling

### Financial Reports
- **Trial Balance**: View all accounts with their debit and credit balances
- **Balance Sheet**: Assets, Liabilities, and Equity with proper categorization
- **Income Statement**: Revenue and Expenses with Net Income calculation
- **General Ledger**: Detailed transaction history by account with running balances
- **CSV Export**: Export any report to CSV for external analysis

### Dashboard
- **Quick Statistics**: Total Assets, Liabilities, Net Worth, and Account Count
- **Financial Summaries**: Key metrics from Balance Sheet and Income Statement
- **Recent Transactions**: Quick view of the latest 10 transactions
- **Account Type Breakdown**: Visual count of accounts by type

### Advanced Filtering
- **Date Range Filters**: Filter transactions by date with preset options (Today, This Week, This Month, This Year, All Time)
- **Account Filters**: Filter by specific account
- **Amount Range**: Filter transactions by minimum and maximum amounts
- **Description Search**: Search transactions by description with debounced input

### Multi-Language Support (i18n)
Fully translated interface in 5 languages:
- 🇬🇧 English
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇨🇳 Chinese (中文)
- 🇵🇹 Portuguese (Português)

All UI elements, reports, and error messages are translated.

### Data Management
- **LocalStorage Persistence**: All data stored in browser LocalStorage
- **Import/Export**: Backup and restore your data with JSON files
- **Data Validation**: Comprehensive form validation with inline error messages
- **Transaction Balance Validation**: Ensures debits equal credits before submission

### User Experience
- **Dark Mode**: Toggle between light and dark themes
- **Keyboard Shortcuts**:
  - `Ctrl+N` / `Cmd+N`: New Account
  - `Ctrl+Shift+N` / `Cmd+Shift+N`: New Transaction
  - `Ctrl+D` / `Cmd+D`: Go to Dashboard
  - `Ctrl+,` / `Cmd+,`: Open Settings
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Toast Notifications**: User feedback for all actions
- **FAB Buttons**: Quick access to create accounts and transactions
- **Smooth Animations**: Transitions and hover effects throughout

### UI/UX Features
- **Material Design 3**: Modern, clean interface with elevation system
- **Emerald Theme**: Primary color scheme with proper contrast ratios
- **JetBrains Mono Font**: Monospace font for better readability of numbers and codes
- **Sticky Header**: Navigation stays visible while scrolling
- **Modal Forms**: Overlay forms for account and transaction creation
- **Confirmation Dialogs**: Prevents accidental data deletion

## 📦 Quick Start

> **📖 Looking for a shorter guide?** Check out [`QUICK_START.md`](QUICK_START.md) for a concise reference!

### One-line install and run (with uv):
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Then from the project directory:
uv sync && uv run reflex init && uv run reflex run
```

That's it! The app will be available at `http://localhost:3000` 🎉

## 📦 Installation

### Why uv?
`uv` is an extremely fast Python package installer and resolver (10-100x faster than pip). It handles virtual environments automatically, ensures reproducible builds, and makes Python development smoother.

### Prerequisites
- Python 3.13 or higher (3.13 recommended for best compatibility)
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer

### Install uv (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup and Run

1. **Clone or navigate to the project directory:**
```bash
cd offline-ledger
```

2. **Install dependencies using uv:**
```bash
uv sync
```

3. **Initialize the Reflex app (first time only):**
```bash
uv run reflex init
```

4. **Run the development server:**
```bash
uv run reflex run
```

The app will be available at `http://localhost:3000`

### Alternative: Using pip (if you prefer)
```bash
pip install -r requirements.txt
reflex init  # First time only
reflex run
```

## 🛠️ Development Commands

Once you have uv installed and dependencies synced, you can use these commands:

```bash
# Run the development server
uv run reflex run

# Run in production mode
uv run reflex run --env prod

# Export the app as a standalone build
uv run reflex export

# Clear the Reflex cache
uv run reflex init --reset

# Add a new dependency
uv add package-name

# Remove a dependency
uv remove package-name

# Update all dependencies
uv sync --upgrade
```

## 🏗️ Project Structure

```
offline-ledger/
├── app/
│   ├── __init__.py
│   ├── app.py              # Main application and routing
│   ├── state.py            # Application state and business logic
│   ├── components.py       # Reusable UI components
│   ├── dashboard.py        # Dashboard view and components
│   ├── reports.py          # Financial reports components
│   ├── settings.py         # Settings modal
│   └── i18n.py             # Translation strings
├── assets/                 # Static assets
├── .gitignore
├── .python-version        # Python version specification for uv
├── pyproject.toml         # Project configuration and dependencies (uv)
├── rxconfig.py            # Reflex configuration
├── requirements.txt       # Python dependencies (legacy, use pyproject.toml)
├── plan.md               # Development plan (all phases completed ✅)
├── QUICK_START.md        # Quick reference guide for getting started
├── TROUBLESHOOTING.md    # Common issues and solutions
└── README.md             # This file (comprehensive documentation)
```

## 🎯 Usage

### Creating Accounts
1. Click the "+" FAB button (user icon) or press `Ctrl+N`
2. Enter account name, code, and select type
3. Click "Create Account"

### Creating Transactions
1. Click the "+" FAB button (file icon) or press `Ctrl+Shift+N`
2. Enter date and description
3. Add entries with accounts, debits, and credits
4. Ensure debits equal credits (balance shows green when matched)
5. Click "Create Transaction"

### Viewing Reports
1. Navigate to the "Reports" tab
2. Select report type (Trial Balance, Balance Sheet, Income Statement, or General Ledger)
3. Adjust date filters as needed
4. Export to CSV or print

### Dashboard
1. Navigate to the "Dashboard" tab (or press `Ctrl+D`)
2. View key financial metrics at a glance
3. See recent transactions and account type breakdown

### Changing Language
1. Click the language dropdown in the header
2. Select your preferred language
3. The entire interface will update immediately

### Dark Mode
1. Click the moon/sun icon in the header
2. Toggle between light and dark themes

## 📊 Accounting Principles

This application follows standard double-entry accounting principles:

### Account Types and Normal Balances
- **Assets**: Increase with debits, decrease with credits (normal debit balance)
- **Liabilities**: Increase with credits, decrease with debits (normal credit balance)
- **Equity**: Increase with credits, decrease with debits (normal credit balance)
- **Revenue**: Increase with credits, decrease with debits (normal credit balance)
- **Expenses**: Increase with debits, decrease with credits (normal debit balance)

### Accounting Equation
**Assets = Liabilities + Equity**

The application validates this equation on the Balance Sheet report.

### Double-Entry System
Every transaction must have:
- At least two entries (one debit and one credit)
- Total debits equal total credits
- Proper categorization of accounts

## 🔧 Technical Details

### Technologies
- **Package Manager**: uv (fast Python package installer)
- **Framework**: Reflex (Python-based full-stack framework)
- **Frontend**: React (generated by Reflex)
- **Styling**: Tailwind CSS v3
- **Storage**: Browser LocalStorage
- **Font**: JetBrains Mono (from Google Fonts)

### State Management
- Centralized state in `AppState` class
- Computed properties for derived data (reports, balances)
- LocalStorage sync for persistence
- Reactive updates across components

### Data Structure
```python
Account = {
    "id": str,
    "name": str,
    "code": str,
    "type": "Asset" | "Liability" | "Equity" | "Revenue" | "Expense",
    "balance": float
}

Transaction = {
    "id": str,
    "date": str (ISO format),
    "description": str,
    "entries": [
        {
            "account_id": str,
            "debit": float,
            "credit": float
        }
    ]
}
```

## 🚦 Development Status

All phases of the development plan have been completed:

- ✅ Phase 1: Core Accounting Structure & Data Models
- ✅ Phase 2: Advanced Filtering & Transaction Management
- ✅ Phase 3: Offline Storage & PouchDB Integration
- ✅ Phase 4: Internationalization (i18n) - Multi-Language Support
- ✅ Phase 5: Reports & Financial Statements
- ✅ Phase 6: UI Polish & Material Design Implementation
- ✅ Phase 7: Data Validation & User Experience

See `plan.md` for detailed feature breakdown.

## 🎨 Design Philosophy

- **Offline-First**: Works without internet connection, all data stored locally
- **User-Friendly**: Clear, intuitive interface with helpful feedback
- **Fast**: Instant updates with reactive state management
- **Accessible**: Keyboard shortcuts, proper contrast ratios, and semantic HTML
- **International**: Support for multiple languages and locales
- **Modern**: Material Design 3 principles with smooth animations

## 📝 Future Enhancements

Potential features for future versions:
- PDF export for reports
- Charts and visualizations
- Budget tracking and forecasting
- Multi-company support
- Tags and categories for transactions
- Recurring transactions
- Bank reconciliation
- Cash flow statement
- Audit trail and transaction history
- Cloud sync with CouchDB

## 🤝 Contributing

This is a demonstration project showcasing a complete accounting application built with Reflex. Feel free to use it as a reference or starting point for your own projects.

## 📄 License

MIT License - Feel free to use this code for your own projects.

## 💡 Tips

### Performance
- The app uses LocalStorage for persistence - no backend required!
- All computations happen client-side for instant updates
- Dark mode preference is saved automatically

### Data Safety
- Export your data regularly using the Settings → Export feature
- Backup files are in JSON format and can be edited manually if needed
- Import/Export works across different browsers and devices

### Keyboard Shortcuts
Remember these time-savers:
- `Ctrl/Cmd + N` - New Account
- `Ctrl/Cmd + Shift + N` - New Transaction
- `Ctrl/Cmd + D` - Dashboard
- `Ctrl/Cmd + ,` - Settings

## 🙏 Acknowledgments

- Built with [Reflex](https://reflex.dev/)
- Package management with [uv](https://docs.astral.sh/uv/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Font: [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- Icons: [Lucide Icons](https://lucide.dev/)

---

**Made with ❤️ using Reflex + uv**


