import React from "react";
import "./seats.css";

/**
 * NOTE ON SEAT ORDER:
 * - Because your Seat model has no row/col/deck, we map seats in array order.
 * - For "SS" (Sleeper+Seater) and "Sleeper", we split the array in half:
 *   upper = first half, lower = second half.
 * - If you later add row/col/deck in DB, we can place precisely.
 */

export default function SeatsView({ seats = [], schedule, picked, setPicked }) {
  const price = Number(schedule?.fare_amount || 0);
  const category = (schedule?.bus_details?.category_name || "").toLowerCase();

  const isSeater = category.includes("seater") && !category.includes("sleeper");
  const isSleeper = category.includes("sleeper") && !category.includes("seater");
  const isCombo = category.includes("sleeper") && category.includes("seater"); // SS

  const tryPick = (seat) => {
    if (!seat?.is_available) return;
    setPicked(seat);
  };

  // Split into upper/lower for sleeper & combo (SS)
  const mid = Math.ceil(seats.length / 2);
  const upper = seats.slice(0, mid);
  const lower = seats.slice(mid);

  return (
    <div className="rb-container">
      <h2 className="rb-title">
        Select Your Seat — {schedule?.bus_details?.name}{" "}
        <span className="rb-cat">({schedule?.bus_details?.category_name})</span>
      </h2>

      <SeatLegend />

      {isSeater && (
        <div className="rb-deck">
          <DeckHeader label="Seater Layout" />
          <Driver />
          <Seater2x2 seats={seats} picked={picked} price={price} onPick={tryPick} />
        </div>
      )}

      {isSleeper && (
        <div className="rb-decks">
          <div className="rb-deck">
            <DeckHeader label="Upper (Sleeper)" />
            <Driver up />
            <Sleeper2x2 seats={upper} picked={picked} price={price} onPick={tryPick} />
          </div>
          <div className="rb-deck">
            <DeckHeader label="Lower (Sleeper)" />
            <Driver />
            <Sleeper2x2 seats={lower} picked={picked} price={price} onPick={tryPick} />
          </div>
        </div>
      )}

      {isCombo && (
        <div className="rb-decks">
          <div className="rb-deck">
            <DeckHeader label="Upper (Sleeper)" />
            <Driver up />
            <Sleeper2x2 seats={upper} picked={picked} price={price} onPick={tryPick} />
          </div>

          <div className="rb-deck">
            <DeckHeader label="Lower (Seater)" />
            <Driver />
            <Seater2x2 seats={lower} picked={picked} price={price} onPick={tryPick} />
          </div>
        </div>
      )}

      <SummaryBar picked={picked} price={price} />
    </div>
  );
}

/* ---------- Layout helpers (RedBus-style rows with an aisle) ---------- */

function chunkIntoRows(list, seatsPerRow) {
  const rows = [];
  for (let i = 0; i < list.length; i += seatsPerRow) {
    rows.push(list.slice(i, i + seatsPerRow));
  }
  return rows;
}

/** Seater 2x2: [L1, L2]  aisle  [R1, R2] per row */
function Seater2x2({ seats, picked, price, onPick }) {
  // 4 per row, split 2|2 with aisle gap
  const rows = chunkIntoRows(seats, 4);
  return (
    <div className="rb-bus">
      {rows.map((row, idx) => {
        const left = row.slice(0, 2);
        const right = row.slice(2, 4);
        return (
          <div className="rb-row" key={idx}>
            <div className="rb-side">
              {left.map((s) => (
                <SeaterSeat key={s?.id} seat={s} picked={picked} price={price} onPick={onPick} />
              ))}
            </div>
            <div className="rb-aisle" />
            <div className="rb-side">
              {right.map((s) => (
                <SeaterSeat key={s?.id} seat={s} picked={picked} price={price} onPick={onPick} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/** Sleeper horizontal 2x2: [🛏 🛏] aisle [🛏 🛏] per row */
function Sleeper2x2({ seats, picked, price, onPick }) {
  // 4 per row, but each sleeper is a wide rectangle
  const rows = chunkIntoRows(seats, 4);
  return (
    <div className="rb-bus">
      {rows.map((row, idx) => {
        const left = row.slice(0, 2);
        const right = row.slice(2, 4);
        return (
          <div className="rb-row" key={idx}>
            <div className="rb-side">
              {left.map((s) => (
                <SleeperSeat key={s?.id} seat={s} picked={picked} price={price} onPick={onPick} />
              ))}
            </div>
            <div className="rb-aisle" />
            <div className="rb-side">
              {right.map((s) => (
                <SleeperSeat key={s?.id} seat={s} picked={picked} price={price} onPick={onPick} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ---------- Seat atoms ---------- */

function SeaterSeat({ seat, picked, price, onPick }) {
  if (!seat) return <div className="rb-seat rb-empty" />;
  const sold = !seat.is_available;
  const selected = picked?.id === seat.id;
  const cls = [
    "rb-seat",
    sold ? "rb-sold" : "rb-available",
    selected ? "rb-selected" : "",
  ].join(" ");
  return (
    <button className={cls} disabled={sold} onClick={() => onPick(seat)}>
      <div className="rb-seat-no">{seat.seat_number}</div>
      {!sold ? <div className="rb-seat-price">₹{price}</div> : <div className="rb-sold-mark">X</div>}
    </button>
  );
}

function SleeperSeat({ seat, picked, price, onPick }) {
  if (!seat) return <div className="rb-sleeper rb-empty" />;
  const sold = !seat.is_available;
  const selected = picked?.id === seat.id;
  const cls = [
    "rb-sleeper",
    sold ? "rb-sold" : "rb-available",
    selected ? "rb-selected" : "",
  ].join(" ");
  return (
    <button className={cls} disabled={sold} onClick={() => onPick(seat)}>
      <div className="rb-seat-no">{seat.seat_number}</div>
      {!sold ? <div className="rb-seat-price">₹{price}</div> : <div className="rb-sold-mark">X</div>}
    </button>
  );
}

/* ---------- UI bits ---------- */

function DeckHeader({ label }) {
  return <h3 className="rb-deck-title">{label}</h3>;
}

function Driver({ up = false }) {
  return (
    <div className="rb-driver">
      <span className="rb-wheel">🛞</span>
      <span className="rb-driver-text">{up ? "Driver (Upper view)" : "Driver"}</span>
    </div>
  );
}

function SeatLegend() {
  return (
    <div className="rb-legend">
      <LegendItem colorClass="rb-box-available" label="Available" />
      <LegendItem colorClass="rb-box-selected" label="Selected" />
      <LegendItem colorClass="rb-box-sold" label="Sold" />
    </div>
  );
}
function LegendItem({ colorClass, label }) {
  return (
    <div className="rb-legend-item">
      <span className={`rb-box ${colorClass}`} />
      <span>{label}</span>
    </div>
  );
}

function SummaryBar({ picked, price }) {
  return (
    <div className="rb-summary">
      <div className="rb-summary-left">
        {picked ? (
          <>
            ✅ <strong>{picked.seat_number}</strong> • <span className="rb-price">₹{price}</span>
          </>
        ) : (
          <>No seat selected</>
        )}
      </div>
      <button
        className="rb-cta"
        disabled={!picked}
        onClick={() => window.dispatchEvent(new CustomEvent("seat.proceed"))}
      >
        Proceed
      </button>
    </div>
  );
}
