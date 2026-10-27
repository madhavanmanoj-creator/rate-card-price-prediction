# Capstone 11.1: Draft problem statement

## Context
Courier customers negotiate a rate card with the carrier: a price per origin-to-destination lane and weight band. I work on a pricing simulator (Rate Simulator Pro) that lets an analyst test how a change to those rates affects revenue and volume.

## Who is affected
Pricing analysts and account managers who review contracts at renewal. Today they judge whether a lane is priced sensibly by experience and by scrolling through spreadsheets that can hold thousands of rows.

## The decision this work should support
At renewal, which lanes need a conversation because their price doesn't look like the price of similar lanes?

## Proposed question
Using only how a rate card is built (product, region, route type, zones, weight rules), can we predict the price on its first weight slab closely enough to spot lanes that look unusual?

## Why it's worth solving
A consistent "does this look normal?" check saves analyst time, catches slips such as a mistyped rate, and makes discounts visible so they can be defended or corrected deliberately.

## Data I expect to use
A synthetic table of about 1,300 lanes that copies the layout of a real rate-card export from the Rate Simulator project. Real files name customers and carry negotiated prices, so they stay private and a simulated dataset is published instead.

## First idea for success
A regression model that clearly beats a naive guess on customers it has never seen.
