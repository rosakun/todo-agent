Add this line to your repository README.md after Pages is published:

Published site: https://<USERNAME>.github.io/<REPO_NAME>/  (served via HTTPS)

Replace <USERNAME> with your GitHub username or organization and <REPO_NAME> with the repository name. Example:

Published site: https://alice.github.io/differential-privacy-pros-cons/

If you prefer an automatic README edit, run the following locally after confirming the Pages URL works:

1. git pull origin main
2. sed -i '' -e "s|$|\n\nPublished site: https://<USERNAME>.github.io/<REPO_NAME>/|" README.md
3. git add README.md
4. git commit -m "Add published site URL to README"
5. git push origin main

If your repository uses a different default branch, replace 'main' with that branch name.