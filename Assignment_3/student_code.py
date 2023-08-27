import read, copy
from util import *
from logical_classes import *
from copy import deepcopy

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # Student code goes here
        # Checking whether the input statement is a fact or not
        # This would be an essential step for retraction

        if isinstance(fact_rule, Fact):
            # Checking the fact is in the kb
            if fact_rule in self.facts:
                # all the facts are stored inside a list data structure
                index_fact = self.facts.index(fact_rule)
                dfact = self.facts[index_fact]

            # After understanding the fact class, each fact has an attribute support_facts
            for new_fact in dfact.support_facts:
                for i, pair in enumerate(new_fact.supported_by):
                    if pair[1].statement == dfact.statement:
                        new_fact.supported_by.pop(i)
                    if len(new_fact.supported_by) == 0:
                        # Recurssively call the new_fact to retract the any another supported statement
                        self.kb_retract(new_fact)

            # After understanding the fact class, each fact has an attribute support_rules
            for new_rule in dfact.support_rules:
                for i, pair in enumerate(new_fact.supported_by):
                    if pair[1].statement == dfact.statement:
                        new_fact.supported_by.pop(i)
                    if len(new_rule.supported_by) == 0:
                        self.kb_retract(new_rule)

            self.facts.remove(dfact)

        elif isinstance(fact_rule, Rule):
            if fact_rule in self.rules:
                index_rule = self.rules.index(fact_rule)
                drule = self.rules[index_rule]

            for new_fact in drule.supports_facts:
                for i, pair in enumerate(new_fact.supported_by):
                    if drule in pair:
                        new_fact.supported_by.pop(i)
                    if len(new_fact.supported_by) == 0:
                        self.kb_retract(new_fact)

            for new_rule in drule.supports_rules:
                for i, pair in enumerate(new_rule.supported_by):
                    if drule in pair:
                        new_rule.supported_by.pop(i)

                    if len(new_rule.supported_by) == 0:
                        self.kb_retract(new_rule)

            self.rules.remove(drule)

        elif factq(fact_rule):
            if fact_rule in self.facts:
                # all the facts are stored inside a list data structure
                index_fact = self.facts.index(fact_rule)
                dfact = self.facts[index_fact]

            # After understanding the fact class, each fact has an attribute support_facts
            for new_fact in dfact.support_facts:
                for i, pair in enumerate(new_fact.supported_by):
                    if pair[1].statement == dfact.statement:
                        new_fact.supported_by.pop(i)
                    if len(new_fact.supported_by) == 0:
                        # Recurssively call the new_fact to retract the any another supported statement
                        self.kb_retract(new_fact)

            # After understanding the fact class, each fact has an attribute support_rules
            for new_rule in dfact.support_rules:
                for i, pair in enumerate(new_fact.supported_by):
                    if pair[1].statement == dfact.statement:
                        new_fact.supported_by.pop(i)
                    if len(new_rule.supported_by) == 0:
                        self.kb_retract(new_rule)
            self.facts.remove(dfact)
            
            


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        bindings = match(rule.lhs[0], fact.statement)
        pair = []
        pair.append(rule)
        pair.append(fact)

        if bindings:
            new_fact = copy.deepcopy(Fact(instantiate(rule.rhs, bindings)))
            # new_fact = Fact(instantiate(rule.rhs, bindings))
            new_fact.supported_by.append(pair)

            i = kb.facts.index(fact)
            kb.facts[i].supports_facts.append(new_fact)
            j = kb.rules.index(rule)
            kb.rules[j].supports_facts.append(new_fact)

            kb.kb_add(new_fact)
        else:
            lhs = map(lambda x: instantiate(x, bindings), rule.lhs[1:])
            rhs = instantiate(rule.rhs, bindings)
            #new_rule = copy.deepcopy(rule)
            new_rule=Rule([lhs,rhs],[[rule,fact]])

            i = kb.facts.index(fact)
            kb.facts[i].supports_rules.append(new_rule)
            j = kb.rules.index(rule)
            kb.rules[j].supports_rules.append(new_rule)

            kb.kb_add(new_rule)