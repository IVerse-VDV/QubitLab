# Security Policy

## Supported Versions

QubitLab is currently in active development. We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest (main branch) | :white_check_mark: |
| Older releases | :x: |

We recommend always using the latest version from the main branch to ensure you have the most recent security patches and updates.

## Reporting a Vulnerability

The QubitLab team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings and will make every effort to acknowledge your contributions.

### How to Report

If you discover a security vulnerability in QubitLab, please report it by emailing our security team at [**QubitLab Reporting**](https://docs.google.com/forms/d/e/1FAIpQLScrOgm5mq7kqKmCvOVHTJFeK9WrJTnBmSTm5yA-1goh_1CkSA/viewform?usp=dialog). Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### What to Include

When reporting a vulnerability, please include the following information to help us understand and address the issue quickly:

- **Description:** A clear description of the vulnerability and its potential impact
- **Steps to Reproduce:** Detailed steps to reproduce the vulnerability, including any specific configurations or inputs required
- **Affected Components:** Which files, functions, or features are affected
- **Potential Impact:** Your assessment of the severity and potential consequences
- **Suggested Fix:** If you have ideas for how to fix the vulnerability, please include them (optional)
- **Your Contact Information:** Email address for follow-up communication

### Response Timeline

We aim to respond to security reports according to the following timeline:

- **Initial Response:** Within 48 hours of receiving your report, we will acknowledge receipt and provide an initial assessment
- **Investigation:** Within 7 days, we will investigate the vulnerability and determine its severity and scope
- **Resolution:** We will work to develop and test a fix as quickly as possible, with timelines depending on severity:
  - Critical vulnerabilities: Patch within 7 days
  - High severity: Patch within 14 days
  - Medium/Low severity: Patch in next scheduled release
- **Disclosure:** After a fix is deployed, we will publicly disclose the vulnerability details with appropriate credit to the reporter (if desired)

### What to Expect

After reporting a vulnerability, you can expect:

- Confirmation that we received your report
- Regular updates on our progress investigating and fixing the issue
- Credit in our security advisories (if you wish to be acknowledged)
- Coordination on public disclosure timing to ensure users have time to update

## Security Best Practices for Users

While using QubitLab, we recommend following these security best practices:

### For Local Deployment

- Keep Python and all dependencies updated to their latest versions by running `pip install --upgrade -r requirements.txt` regularly
- Use virtual environments to isolate QubitLab dependencies from other Python projects
- Do not expose the Streamlit development server to the public internet—it is intended for local use only
- Review the source code before running if you have security concerns, as QubitLab is open source and transparent

### For Dependency Security

- Regularly check for security advisories for our dependencies (Qiskit, Streamlit, Plotly, NumPy, Matplotlib)
- Use tools like `pip-audit` or `safety` to scan for known vulnerabilities in installed packages:
  ```bash
  pip install pip-audit
  pip-audit
  ```
- Report any vulnerable dependencies you discover so we can update `requirements.txt`

### For Code Contributions

- Review the code you're contributing for potential security issues before submitting pull requests
- Avoid introducing dependencies with known security vulnerabilities
- Do not commit sensitive information (API keys, passwords, personal data) to the repository
- Use the `.gitignore` file to prevent accidentally committing sensitive files

## Known Security Considerations

### Quantum Circuit Execution

QubitLab simulates quantum circuits using Qiskit Aer on classical hardware. All simulations run locally on the user's machine. There are no security risks associated with the quantum simulation itself, as it is purely computational.

### User Input Validation

QubitLab accepts user input for circuit construction through the Streamlit interface. All inputs are validated and constrained to valid quantum operations. Users cannot execute arbitrary code or access system resources through the application interface.

### Data Privacy

QubitLab does not collect, store, or transmit any user data. All quantum circuit construction and simulation happens entirely on the user's local machine. No information is sent to external servers. However, Streamlit may collect anonymous usage analytics if configured—refer to Streamlit's privacy policy for details.

### Third-Party Dependencies

QubitLab relies on several third-party Python packages. While we strive to keep dependencies updated, we cannot control the security of these external projects. Users should be aware that security vulnerabilities may exist in dependencies and should keep their installations updated.

## Security Updates

When security vulnerabilities are discovered and fixed, we will:

- Release a patched version immediately for critical vulnerabilities
- Publish a security advisory on GitHub describing the vulnerability, its impact, and the fix
- Update the `requirements.txt` file if the vulnerability is in a dependency
- Notify users through GitHub release notes and repository announcements

Subscribe to repository releases and watch the repository to receive notifications about security updates.

## Scope

This security policy applies to:

- The QubitLab application code in this repository (app.py, gates.py, utils.py)
- Configuration files and documentation
- The deployment and usage instructions provided

This security policy does not cover:

- Third-party dependencies (report to their respective maintainers)
- User modifications or forks of QubitLab
- Issues arising from improper deployment or configuration
- Quantum computing concepts or algorithms (these are educational demonstrations, not production systems)

## Contact

For security-related inquiries, contact:

**Email:** furtzfarry@gmail.com
**Organization:** IVerse-VDV  
**Project:** QubitLab

For non security issues, please use the standard GitHub issues or discussions channels.

---

Thank you for helping keep QubitLab and its users secure. Your responsible disclosure of security vulnerabilities helps protect the entire community and contributes to the project's reliability and trustworthiness.
