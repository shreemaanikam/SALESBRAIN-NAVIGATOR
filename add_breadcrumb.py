import os
import re

content = """
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
"""

# Let's write a python script to patch dashboard/layout.tsx
