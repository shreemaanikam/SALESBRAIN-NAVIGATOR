import re
file_path = "frontend/src/app/page.tsx"
with open(file_path, "r") as f:
    content = f.read()

how_it_works = """
        </section>

        {/* ── How it Works ── */}
        <section id="how-it-works" className="py-24 bg-slate-50 dark:bg-slate-800/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">How SalesBrain Works</h2>
              <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">From raw data to actionable insights in three simple steps.</p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">1</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Connect Data</h3>
                <p className="text-slate-600 dark:text-slate-400">Upload your CSV dataset. SalesBrain securely processes it locally without sending it to external APIs.</p>
              </div>
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">2</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Auto-Generate KPIs</h3>
                <p className="text-slate-600 dark:text-slate-400">Our engine instantly creates a dynamic dashboard with your revenue, margins, and regional performance trends.</p>
              </div>
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">3</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Get ML Insights</h3>
                <p className="text-slate-600 dark:text-slate-400">Leverage our Ridge regression models to predict profitability and uncover hidden growth opportunities.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Security Section */}
"""

content = content.replace('</section>\n\n        {/* Security Section */}', how_it_works)

with open(file_path, "w") as f:
    f.write(content)

