# Evaluation Tests for Customer Service Agent

This directory contains evaluation tests for the Cymbal Home & Garden customer service agent.

## Overview

The evaluation framework tests the agent's ability to handle realistic customer service conversations using the Google ADK evaluation system.

## Test Files

### `eval_data/simple.test.json`
A basic test that verifies:
- Greeting functionality
- Cart information retrieval

**Usage:**
```bash
pytest eval/test_eval.py::test_eval_simple -v
```

### `eval_data/full_conversation.test.json`
A comprehensive test that covers the complete customer service flow:

1. **Greeting** - Agent welcomes customer
2. **Product Inquiry** - Customer asks about sunflower seeds
3. **Department Browsing** - Customer asks what other seeds are available
4. **Add to Cart** - Customer adds 2 sunflower seed packets
5. **Check Cart** - Customer verifies cart contents
6. **Add More Items** - Customer adds a hand trowel
7. **Remove Items** - Customer removes tomato seeds
8. **Verify Final Cart** - Customer checks final cart before checkout
9. **Goodbye** - Polite conversation closure

**Tools Tested:**
- `check_product_list` - Browse products by department
- `modify_cart` - Add and remove items with quantities
- `access_cart_information` - View current cart state

**Usage:**
```bash
pytest eval/test_eval.py::test_eval_full_conversation -v
```

### `eval_data/cart_management.test.json`
A focused test for cart operations (shorter to avoid rate limits):

1. **Greeting** - Basic welcome
2. **Add to Cart** - Add 2 sunflower seed packets
3. **Check Cart** - Verify cart contents
4. **Remove Item** - Remove tomato seeds

**Tools Tested:**
- `modify_cart` - Add and remove items
- `access_cart_information` - View cart

**Usage:**
```bash
pytest eval/test_eval.py::test_eval_cart_management -v
```

## Running All Tests

```bash
pytest eval/test_eval.py -v
```

## Important Notes

### Rate Limiting
The Vertex AI API has rate limits. If you see `429 RESOURCE_EXHAUSTED` errors:
- Run tests individually rather than all at once
- Add delays between test runs
- Keep test conversations shorter (4-6 turns max)
- The `full_conversation.test.json` has 8 turns and may hit rate limits

### Test Separately
```bash
# Run one at a time with delays
pytest eval/test_eval.py::test_eval_simple -v
sleep 30
pytest eval/test_eval.py::test_eval_cart_management -v
```

