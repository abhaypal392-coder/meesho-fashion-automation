# Meesho Fashion Affiliate Cloud Starter

This is a **starter workflow**, not a ready-to-run Meesho or Instagram integration.
It can run on GitHub Actions while your laptop is off, on a schedule, using the free GitHub Actions allowance subject to account limits.

## What it does now
- Reads a manually approved `products/products.csv` file.
- Creates a clean promotional banner for each approved product.
- Writes a caption draft and a daily report.
- Saves output as a workflow artifact for review/download.

## What it does NOT do yet
- It does not scrape Meesho.
- It does not create or verify affiliate links.
- It does not auto-publish to Instagram or send DMs.
- It does not verify purchases or commission.
Those steps need authorized Meesho product/affiliate access and Meta Instagram permissions/tokens. Never share passwords or tokens in source code.

## Quick start
1. Create a GitHub repository and upload these files.
2. Edit `products/products.csv` with products you are authorized to promote.
3. Use the affiliate tracking URL supplied by your approved Meesho creator/affiliate account in `affiliate_url`.
4. Commit the changes to the default branch.
5. Open **Actions** and run `Build daily product creatives` manually.
6. Download the generated `daily-creatives` artifact and review it.
7. The workflow also runs on a daily schedule; GitHub-hosted workflows run in the cloud, so your laptop can be off.

## CSV fields
- `product_name`: product name
- `price_inr`: current verified price
- `category`: e.g. Kurti, Saree, Jewellery, Beauty
- `affiliate_url`: actual approved tracking URL, not a plain product URL
- `image_url`: publicly accessible product image URL you are permitted to use
- `approved`: set to `yes` only after checking the product, price, image rights, and link
- `hook`: short promotional headline

Do not use copyrighted images without permission, false discounts, fake reviews, or unverified claims. Label affiliate content clearly.

## Cloud scheduling
The GitHub Actions workflow runs at 05:30 UTC daily (11:00 AM India time). Scheduled workflows can be delayed by GitHub and are not a guaranteed real-time scheduler. GitHub Free accounts have included Actions usage limits; check current billing/settings.

## Next integration steps
1. Confirm Meesho creator programme access and obtain valid affiliate tracking links through its official portal.
2. Set up an Instagram professional account and Meta developer app, then obtain the required Instagram publishing permissions.
3. Add tokens only as GitHub repository Actions secrets (never commit them).
4. Test with manual approval before enabling auto-publishing.
5. DM automation must only use permitted messaging flows (e.g. responding to user-initiated interactions); do not bulk-message strangers.
