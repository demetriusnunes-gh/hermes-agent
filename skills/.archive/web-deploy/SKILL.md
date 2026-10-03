---
name: web-deploy
description: "Download files and make them available via web server"
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
---

# Web File Deployment

When you need to download files from a URL and make them available for download via a web server.

## Procedure

1. **Download file**: Use curl with -L flag to follow redirects and -O to preserve filename
   ```bash
   curl -L -O <url>
   ```

2. **Verify download**: Check that file was downloaded completely
   ```bash
   ls -lh <filename>
   ```
   Confirm exit code was 0 and file size is reasonable

3. **Copy to web directory**: Transfer file to web server document root
   ```bash
   cp <filename> <web-root-path>/
   ```

4. **Verify placement**: Confirm file exists in correct location
   ```bash
   ls -lh <web-root-path>/<filename>
   ```

5. **Test accessibility**: Verify file can be downloaded via HTTP
   ```bash
   curl -I http://<domain>/<filename>
   ```
   Look for HTTP 200 OK or proper redirect (301/302/308)

## User Preferences

- Provide direct, implementation-oriented answers without unnecessary explanation
- Include verification steps after each operation to ensure success
- Use concrete commands and file paths in responses

## Pitfalls

- **Always verify downloads completed**: Incomplete downloads can cause silent failures; check file size and curl exit code
- **Use absolute paths for web root**: Avoid confusion from relative paths or changing directories
- **Check file permissions**: Ensure web server process can read the deployed file (typically 644)
- **Test with HEAD request**: Use `curl -I` to verify accessibility without downloading file again
- **Follow redirects**: Always use `-L` with curl unless you specifically need to handle redirects manually

## References

- See `references/web-servers.md` for common web root paths across systems
- See `references/curl-options.md` for detailed curl flag explanations
