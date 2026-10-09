import { Link, useParams } from "react-router-dom";
import "./MockDocument.css";

const mockDocuments = {
  identity: {
    title: "Sample Identity Document",
    type: "Identity Proof",
    name: "DEMO CITIZEN",
    number: "XXXX-XXXX-XXXX",
    date: "01 January 1964",
    address: "Demo Village, Demo District, Karnataka"
  },

  income: {
    title: "Sample Income Certificate",
    type: "Income Certificate",
    name: "DEMO CITIZEN",
    number: "DEMO/INC/2026/0001",
    date: "15 September 2026",
    address: "Demo Village, Demo District, Karnataka"
  },

  residence: {
    title: "Sample Residence Certificate",
    type: "Residence Certificate",
    name: "DEMO CITIZEN",
    number: "DEMO/RES/2026/0001",
    date: "20 September 2026",
    address: "Demo Village, Demo District, Karnataka"
  },

  bank: {
    title: "Sample Bank Document",
    type: "Bank Account Proof",
    name: "DEMO CITIZEN",
    number: "XXXX XXXX 1234",
    date: "30 September 2026",
    address: "Demo Branch — Demonstration Only"
  }
};

function MockDocument() {
  const { type } = useParams();

  const document = mockDocuments[type];

  if (!document) {
    return (
      <div className="container mock-not-found">
        <h1>
          Sample Document Not Found
        </h1>

        <Link to="/documents">
          ← Back to Document Centre
        </Link>
      </div>
    );
  }

  return (
    <div className="mock-document-page">

      <section className="mock-page-header">

        <div className="container">

          <Link
            to="/documents"
            className="back-link"
          >
            ← Back to Document Centre
          </Link>

          <span>
            DEMONSTRATION DOCUMENT
          </span>

          <h1>
            {document.title}
          </h1>

        </div>

      </section>


      <section className="mock-document-content">

        <div className="container">

          <div className="mock-warning">

            <strong>
              SAMPLE / DEMO ONLY
            </strong>

            <p>
              This document is fictional and has no legal,
              identification or verification value.
            </p>

          </div>


          <div className="document-paper">

            <div className="document-watermark">
              DEMO
            </div>


            <div className="paper-header">

              <div className="paper-emblem">
                🇮🇳
              </div>

              <div>

                <h2>
                  GOVERNMENT DOCUMENT
                </h2>

                <p>
                  DEMONSTRATION SAMPLE
                </p>

              </div>

            </div>


            <div className="paper-title">

              <h1>
                {document.type}
              </h1>

              <span>
                SAMPLE — NOT VALID
              </span>

            </div>


            <div className="paper-details">

              <div>
                <label>
                  Name
                </label>

                <strong>
                  {document.name}
                </strong>
              </div>


              <div>
                <label>
                  Document Number
                </label>

                <strong>
                  {document.number}
                </strong>
              </div>


              <div>
                <label>
                  Date
                </label>

                <strong>
                  {document.date}
                </strong>
              </div>


              <div>
                <label>
                  Address / Details
                </label>

                <strong>
                  {document.address}
                </strong>
              </div>

            </div>


            <div className="paper-footer">

              <span>
                SAMPLE DOCUMENT
              </span>

              <span>
                NOT VALID FOR OFFICIAL USE
              </span>

            </div>

          </div>

        </div>

      </section>

    </div>
  );
}

export default MockDocument;