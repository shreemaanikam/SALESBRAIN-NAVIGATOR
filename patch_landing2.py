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

        <section id="security" """

content = re.sub(r'</section>\s*<section id="security"', how_it_works, content)

contact = """
        </section>

        {/* ── Request Demo / Contact ── */}
        <section id="contact" className="py-24 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-6">Ready to transform your retail data?</h2>
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-8">Deploy SalesBrain Navigator in your private environment and unlock the power of your data.</p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/dashboard" className="px-8 py-4 bg-blue-600 text-white rounded-full font-semibold text-lg hover:bg-blue-700 transition-colors">
              Try it now
            </Link>
            <a href="mailto:demo@salesbrain.ai" className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-full font-semibold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors border border-slate-200 dark:border-slate-700">
              Contact Sales
            </a>
          </div>
        </section>
      </main>
"""

content = re.sub(r'</section>\s*</main>', contact, content)

with open(file_path, "w") as f:
    f.write(content)

